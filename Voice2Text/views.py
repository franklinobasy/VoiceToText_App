# -*- coding: utf-8 -*-

'''This module provides views for app'''
import speech_recognition as sr

from PyQt5.QtCore import (
    Qt, 
    QSize, 
    QThread,
    pyqtSignal
)

from PyQt5.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton, 
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import (
    QPixmap, 
    QIcon
)

from .properties import *

class Window(QMainWindow):
    ''' The Main Window '''
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle(TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.status = "Inactive"

        self.setUpUi()
    
    def setUpUi(self):
        self.text_output = TextOutput(self)
        self.listen_button = ListenButton(self, self.text_output)
        self.audio_read = ReadAudio(self, self.text_output)
      

        self.layout.addWidget(self.listen_button, alignment= Qt.AlignCenter, )
        self.layout.addStretch()
        self.layout.addWidget(self.audio_read, alignment= Qt.AlignLeft)
        self.layout.addWidget(self.text_output, alignment= Qt.AlignCenter, )
        

class ListenButton(QPushButton):
    def __init__(self, parent= None, label_object = None):
        super().__init__(parent)
        
        self.pixmap = QPixmap(blue_image)
        self.parent = parent
        self.label_object = label_object

        self.setMinimumHeight(200)
        self.setMinimumWidth(200)
        self.setIcon(QIcon(self.pixmap))
        self.setIconSize(QSize(200, 200))
        self.setMouseTracking(True)
        self.clicked.connect(self.press)
        self.setObjectName('Listen')
    
    def leaveEvent(self, event):
        self.setIconSize(QSize(200, 200))

    def enterEvent(self, event):
        self.setIconSize(QSize(225, 225))
    
    def press(self):
        if self.parent.status == 'OFF':
            self.parent.status = 'ON'
            self.pixmap = QPixmap(green_image)
        elif self.parent.status == 'ON':
            self.parent.status = 'OFF'
            self.pixmap = QPixmap(red_image)
        elif self.parent.status == 'Inactive':
            self.parent.status = 'ON'
            self.pixmap = QPixmap(green_image)
        
        self.setIcon(QIcon(self.pixmap))
        self.label_object.setText(f'>>>& STATUS : {self.parent.status}')
        print(self.parent.status)
        

class TextOutput(QLabel):
    def __init__(self, parent= None):
        super().__init__(parent)

        self.setMinimumHeight(100)
        self.setMinimumWidth(WINDOW_WIDTH)
        self.setObjectName('TextOut')
        self.setText(f'>>>& STATUS : {parent.status}')
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setWordWrap(True)


class ReadAudio(QGroupBox):
    def __init__(self, parent= None, label_object= None):
        super().__init__(parent)
        self.setObjectName('AudioContainer')
        self.label_object = label_object

        self.setMinimumHeight(60)
        self.setMinimumWidth(WINDOW_WIDTH)

        self.initialize_elements()

    def initialize_elements(self):
        button = QPushButton('input audio')
        go_button = QPushButton('  Go  ')
        self.path = QLineEdit()
        layout = QHBoxLayout()

        button.resize(12, 4)
        button.setObjectName('AudioButton')
        button.clicked.connect(self.openAudio)
        button.setToolTip('Click here to choose audio from local directory')

        go_button.resize(12, 4)
        go_button.setMinimumWidth(12)
        go_button.setObjectName('AudioButton')
        go_button.clicked.connect(self.startReadAudioFile)
        go_button.setToolTip('Convert audio to text')

        self.path.resize(250, 20)
        self.path.setMinimumWidth(250)
        self.path.setObjectName('AudioButton')
        self.path.setPlaceholderText('Type file path here...')

        layout.addWidget(button, alignment= Qt.AlignLeft)
        layout.addWidget(self.path, alignment=Qt.AlignCenter)
        layout.addWidget(go_button, alignment= Qt.AlignRight)

        self.setLayout(layout)
    
    def openAudio(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "WAV Files (*.wav)")
        if file_name:
            self.path.setText(file_name)
        else:
            QMessageBox.information(self, 'Error', 'Unable to find file, try again!', QMessageBox.Ok)
    
    def startReadAudioFile(self):
        file_path = self.path.text()
        try:
            if not file_path:
                QMessageBox.information(self, 'Error', 'Must enter a file path', QMessageBox.Ok)
                self.path.setFocus()
            else:
                self.label_object.setText('>>> TRANSLATING...')
                self.worker = AudioReadingThread(file_path)
                self.worker.readAudioSignal.connect(self.displayReadAudioFile)
                self.worker.start()
        except sr.RequestError:
            QMessageBox.information(self, 'Error', 'Internet Connection problem, \nEnsure You have a stable internet connection', QMessageBox.Ok)
    
    def displayReadAudioFile(self, output):
        self.label_object.setText(output)


class AudioReadingThread(QThread):
    readAudioSignal = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        r = sr.Recognizer()
        audio_file = sr.AudioFile(self.file_path)
        with audio_file as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source)
        text = r.recognize_google(audio)
        # output = r.recognize_google(audio, show_all=True)
        # output = list(output.values())[0]
        # text = ''
        # for item in output:
        #     item = str(item)
        #     item = item[16:-2]
        #     text = text + str(item) + '\n'
        self.readAudioSignal.emit(text)
        
        


