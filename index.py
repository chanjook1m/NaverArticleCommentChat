import sys
import naver
import config
from PyQt5.QtWidgets import *
from gui import login
from gui import board

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if config.DEBUG:
        naver.login(config.LOGIN_ID, config.LOGIN_PW)
    else:
        loginUI = login.Window()
        loginUI.show()
        app.exec_()

    boardUI = board.Window()
    boardUI.show()
    app.exec_()
