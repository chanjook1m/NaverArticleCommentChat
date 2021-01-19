from PyQt5.QtCore import *
import time
import random
import naver
import config


class Worker(QThread):
    finished = pyqtSignal(list)

    def __init__(self, articleId):
        super().__init__()
        self.articleId = articleId

    def run(self):
        while True:
            comments = naver.main(self.articleId, config.START_PAGE_NUM)
            if comments is not None:
                self.finished.emit(comments)
            time.sleep(random.uniform(30, 45))

    def runOnce(self):
        comments = naver.main(self.articleId, config.START_PAGE_NUM)
        if comments is not None:
            self.finished.emit(comments)
