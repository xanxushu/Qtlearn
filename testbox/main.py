import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QMainWindow,QPushButton
from translator import TranslatorUI,APP_ID,APP_KEY,URL,LANG_CODES,LANGUAGES
from offices import ExcelViz
from apitest import App,ImageDownloader
import face_recognize
from qrcoder import QrcodeApp
from iper import IPQueryApp

class main_ui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)

        self.firstline_layout =QHBoxLayout()
        self.mainlayout.addLayout(self.firstline_layout)
        self.office_choice_button = QPushButton(text='excel数据可视化')
        self.firstline_layout.addWidget(self.office_choice_button)
        self.office_choice_button.clicked.connect(self.show_excel)
        self.translator_chioce_button =QPushButton(text='简单翻译器')
        self.firstline_layout.addWidget(self.translator_chioce_button)
        self.translator_chioce_button.clicked.connect(self.show_translator)

        self.secline_layout = QHBoxLayout()
        self.mainlayout.addLayout(self.secline_layout)
        self.imager_choice_button = QPushButton(text='简单图片下载器')
        self.imager_choice_button.clicked.connect(self.show_imager)
        self.secline_layout.addWidget(self.imager_choice_button)
        self.face_choice_button = QPushButton(text='简单人脸识别器')
        self.secline_layout.addWidget(self.face_choice_button)
        self.face_choice_button.clicked.connect(face_recognize.show_window)

        self.thiline_layout =QHBoxLayout()
        self.mainlayout.addLayout(self.thiline_layout)
        self.qrcoder_choice_button = QPushButton(text='简单二维码生成器')
        self.qrcoder_choice_button.clicked.connect(self.show_qrcoder)
        self.thiline_layout.addWidget(self.qrcoder_choice_button)
        self.iper_choice_button = QPushButton(text='IP查询')
        self.iper_choice_button.clicked.connect(self.show_iper)
        self.thiline_layout.addWidget(self.iper_choice_button)

    def show_translator(self):
        self.translator = TranslatorUI()
        self.translator.setWindowTitle("简单翻译器")
        self.translator.show()

    def show_excel(self):
        self.excel = ExcelViz()
        self.excel.setWindowTitle("excel数据可视化")
        self.excel.show()

    def show_imager(self):
        self.imager = App()
        self.imager.setWindowTitle("简单图片下载器")
        self.imager.show()

    def show_qrcoder(self):
        self.qrcoder = QrcodeApp()
        self.qrcoder.setWindowTitle("二维码生成器")
        self.qrcoder.show()
    def show_iper(self):
        self.iper = IPQueryApp()
        self.iper.setWindowTitle("IP查询器")
        self.iper.show()

if __name__ == "__main__":   
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = main_ui()
    window.setCentralWidget(ui)
    window.setWindowTitle('小工具箱')
    window.setMinimumSize(1200,600)
    window.show()
    sys.exit(app.exec_())