import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
import naver
import config

ui_path = os.path.dirname(os.path.abspath(__file__))
# login_form = uic.loadUiType(os.path.join(ui_path, "login.ui"))[0]
login_form = uic.loadUiType(
    r"C:\Users\1z3r0\Desktop\봉우리\네이버카페\gui\login.ui")[0]


class Window(QMainWindow, login_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("네이버 로그인")
        self.editId.returnPressed.connect(self.btn_clicked)
        self.editPw.returnPressed.connect(self.btn_clicked)
        self.editPw.setEchoMode(QLineEdit.Password)
        self.loginBtn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        id = self.editId.text()
        pw = self.editPw.text()
        loginMessage = naver.login(id, pw)
        if loginMessage == config.LOGIN_FAILED_MESSAGE:
            QMessageBox.about(self, "실패", loginMessage)
        else:
            self.close()
