# import os
# import time

# # 다운받을 이미지 url
# url = "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/spn/spn02123/l/10.jpg"

# # time check
# start = time.time()

# # curl 요청
# os.system("curl " + url + " > test.jpg")

# # 이미지 다운로드 시간 체크
# print(time.time() - start)



import requests
from PyQt5.QtWidgets import *
from PyQt5 import uic
from posixpath import split
from ntpath import join
import sys, os, requests
from pprint import pprint
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "imagedownloder.ui"

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)

        self.download_pushButton.clicked.connect(self.image_downloder)

        

    def image_downloder(self) :
        image_url = self.URL_lineEdit.text()
        file_name = self.filename_lineEdit.text()
        # 초기 셋팅 함수
        f = open(f'{file_name}.jpg','wb')
        response = requests.get(image_url)
        f.write(response.content)
        f.close()

        img = Image.open(f'{file_name}.jpg')

        img_resize = img.resize((1000, 1000))
        img_resize.save(f'{file_name}.jpg')

        self.status_label.setText("download successful")


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())

