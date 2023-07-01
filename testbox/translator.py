import sys
import requests
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QLabel,
                             QTextEdit, QPushButton, QComboBox)

# 百度翻译api的相关信息，需要替换为自己的
APP_ID = ""
APP_KEY = ""
URL = "http://api.fanyi.baidu.com/api/trans/vip/translate"

# 支持的语言列表，可以根据需要增加或减少
LANGUAGES = ["自动检测", "中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语"]

# 语言代码的映射，用于构造请求参数
LANG_CODES = {
    "自动检测": "auto",
    "中文": "zh",
    "英语": "en",
    "日语": "jp",
    "韩语": "kor",
    "法语": "fra",
    "德语": "de",
    "西班牙语": "spa"
}

class TranslatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 创建输入文本框和选择器
        self.input_layout = QHBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.input_label = QLabel("输入:")
        self.input_layout.addWidget(self.input_label)
        self.input_box = QTextEdit()
        self.input_box.setMinimumSize(800,300)
        self.input_layout.addWidget(self.input_box)
        self.input_selector = QComboBox()
        self.input_selector.addItems(LANGUAGES)
        self.input_selector.setCurrentText("自动检测")
        self.input_layout.addWidget(self.input_selector)

        # 创建输出文本框和选择器
        self.output_layout = QHBoxLayout()
        self.main_layout.addLayout(self.output_layout)
        self.output_label = QLabel("输出:")
        self.output_layout.addWidget(self.output_label)
        self.output_box = QTextEdit()
        self.output_box.setMinimumSize(800,300)
        self.output_box.setReadOnly(True)
        self.output_layout.addWidget(self.output_box)
        self.output_selector = QComboBox()
        self.output_selector.addItems(LANGUAGES)
        self.output_selector.setCurrentText("中文")
        self.output_layout.addWidget(self.output_selector)

        # 创建翻译按钮
        self.translate_button = QPushButton("翻译")
        # 连接按钮的点击信号到槽函数
        self.translate_button.clicked.connect(self.translate)
        self.main_layout.addWidget(self.translate_button)

    def translate(self):
        # 获取输入文本和选择的语言
        input_text = self.input_box.toPlainText()
        from_lang = LANG_CODES[self.input_selector.currentText()]
        to_lang = LANG_CODES[self.output_selector.currentText()]
        
        # 如果输入文本不为空，调用百度翻译api进行翻译
        if input_text:
            # 构造请求参数
            params = {
                "q": input_text,
                "from": from_lang,
                "to": to_lang,
                "appid": APP_ID,
                # 随机数，可以任意设置
                "salt": 12345678,
            }
            # 计算签名，参考百度翻译api文档
            sign = APP_ID + input_text + str(params["salt"]) + APP_KEY
            import hashlib
            m = hashlib.md5()
            m.update(sign.encode("utf-8"))
            sign = m.hexdigest()
            params["sign"] = sign

            # 发送请求并获取响应
            response = requests.get(URL, params=params)
            data = response.json()

            # 如果响应中有翻译结果，显示在输出文本框中
            if "trans_result" in data:
                output_text = data["trans_result"][0]["dst"]
                self.output_box.setText(output_text)
            # 否则显示错误信息
            else:
                self.output_box.setText("翻译失败，请检查网络或输入")
        # 如果输入文本为空，清空输出文本框
        else:
            self.output_box.clear()

    '''def show_translations(self):
        self.setWindowTitle("简单翻译器")
        self.show()
    '''

if __name__ =="__main__":
    app = QApplication(sys.argv)
    # 加载Qt的翻译文件
    qt_translator = QTranslator(app)
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    qt_translator.load(QLocale.system(), 'qtbase', '_', path)
    app.installTranslator(qt_translator)
    # 创建主窗口和界面
    window = QMainWindow()
    ui = TranslatorUI()
    window.setCentralWidget(ui)
    window.setWindowTitle("简单翻译器")
    window = TranslatorUI()
    window.show()
    sys.exit(app.exec_())

