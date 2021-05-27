# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from .views import Window
def main():
    '''App main's function'''
    #load style sheet
    with open('Voice2Text/stylesheet.css') as file:
        stylesheet = file.read()
        file.close()
    # create the application
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    # create window
    window = Window()
    window.show()

    #Run the event loop
    sys.exit(app.exec())