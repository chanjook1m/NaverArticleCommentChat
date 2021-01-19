import sys
import os
import time
import random
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

import naver
import config
import crawling
from gui import login

ui_path = os.path.dirname(os.path.abspath(__file__))
# board_form = uic.loadUiType(os.path.join(ui_path, "board.ui"))[0]
board_form = uic.loadUiType(
    r"C:\Users\1z3r0\Desktop\봉우리\네이버카페\gui\board.ui")[0]

articleId = None


class Window(QMainWindow, board_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("네이버 카페 ver.1.0")
        self.commentProgress.setValue(0)
        self.startBtn.clicked.connect(self.startBtn_clicked)
        self.submitBtn.clicked.connect(self.submitBtn_clicked)
        self.editComment.returnPressed.connect(self.submitBtn_clicked)

    def submitBtn_clicked(self):
        global articleId

        self.commentProgress.setValue(0)
        text = self.editComment.text()
        naver.submitComment(articleId, text)

        try:
            self.worker = crawling.Worker(articleId)
            self.worker.finished.connect(self.update_widget)
            self.worker.runOnce()
        except:
            QMessageBox.about(self, "실패", config.COMMENT_GET_FAILED_MESSAGE)

    def startBtn_clicked(self):
        global articleId

        self.commentProgress.setValue(0)
        self.startBtn.setEnabled(False)
        url = self.editUrl.text()
        articleId = url.split('/')[4]

        try:
            self.worker = crawling.Worker(articleId)
            self.worker.finished.connect(self.update_widget)
            self.worker.start()
        except:
            QMessageBox.about(self, "실패", config.COMMENT_GET_FAILED_MESSAGE)

    @ pyqtSlot(list)
    def update_widget(self, data):
        for comment in data:
            self.commentsList.addItem(comment)
        self.commentProgress.setValue(100)
