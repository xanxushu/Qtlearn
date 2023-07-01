import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QLineEdit, QFileDialog, QPushButton, QLabel, QTextEdit,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from bs4 import BeautifulSoup
import urllib.request


class ImageDownloader(QThread):
    # 定义信号，用来更新爬取过程显示框
    signal = pyqtSignal(str)

    def __init__(self, url_method, url_text, keyword_method, keyword_text, num_text, folder_text, gif_method):
        super().__init__()
        self.url_method = url_method # 网址方法勾选框的状态
        self.url_text = url_text # 网址输入文本框的内容
        self.keyword_method = keyword_method # 关键词方法勾选框的状态
        self.keyword_text = keyword_text # 关键词输入文本框的内容
        self.num_text = num_text # 图片下载数量文本框的内容
        self.folder_text = folder_text # 导出文件夹选择框的内容
        self.gif_method = gif_method # 是否包括动图勾选框的状态

    def run(self):
        # 根据不同的方法执行不同的爬取逻辑
        if self.url_method:
            self.download_by_url()
        elif self.keyword_method:
            self.download_by_keyword()
        else:
            self.signal.emit("请选择一种方法")

    def download_by_url(self):
        # 通过网址爬取图片
        try:
            # 获取网页源码
            response = requests.get(self.url_text)
            response.encoding = response.apparent_encoding
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            # 找到所有图片标签
            imgs = soup.find_all("img")
            # 遍历图片标签，获取图片链接，下载图片并保存到指定文件夹
            for i, img in enumerate(imgs):
                src = img.get("src")
                if src:
                    if src.startswith("//"):
                        src = "http:" + src
                    elif src.startswith("/"):
                        src = self.url_text + src
                    elif src.startswith("data:image/svg+xml;utf8"): # 判断是否是svg格式
                        # 发送信号，更新爬取过程显示框
                        self.signal.emit(f"正在下载第{i+1}张图片：{src}")
                        # 下载图片并保存到指定文件夹，文件名为序号加".svg"后缀
                        urllib.request.urlretrieve(src, self.folder_text + f"/{i+1}.svg")
                        continue # 跳过后面的代码

                    # 判断是否包括动图，如果不包括则跳过gif格式的图片
                    if not self.gif_method and src.endswith(".gif"):
                        continue
                    # 发送信号，更新爬取过程显示框
                    self.signal.emit(f"正在下载第{i+1}张图片：{src}")
                    # 下载图片并保存到指定文件夹，文件名为序号加后缀名
                    src = src.split("?")[0] # 去掉问号及其后面的部分
                    print(src)
                    r = requests.get(src)
                    with open(self.folder_text + f"/{i+1}.{src.split('.')[-1]}", "wb") as f:
                        f.write(r.content)
            # 发送信号，更新爬取过程显示框，显示爬取成功信息
            self.signal.emit(f"爬取成功，共下载了{len(imgs)}张图片")
        except Exception as e:
            # 发送信号，更新爬取过程显示框，显示爬取失败信息和异常信息
            self.signal.emit(f"爬取失败，原因：{e}")

    def download_by_keyword(self):
        # 通过关键词爬取图片
        try:
            # 定义百度图片和必应图片的搜索链接前缀和后缀
            baidu_prefix = "https://image.baidu.com/search/index?tn=baiduimage&word="
            baidu_suffix = "&pn="
            bing_prefix = "https://cn.bing.com/images/search?q="
            bing_suffix = "&first="
            # 计算每个搜索引擎需要爬取的页数（每页30张图片）
            num = int(self.num_text)
            pages = (num - 1) // 30 + 1
            # 定义一个计数器，用来记录下载的图片数量和文件名序号
            count = 0
            # 遍历每个搜索引擎和每个页数，获取网页源码，找到所有图片标签，获取图片链接，下载图片并保存到指定文件夹
            for prefix, suffix in [(baidu_prefix, baidu_suffix), (bing_prefix, bing_suffix)]:
                for page in range(pages):
                    # 获取网页源码
                    response = requests.get(prefix + self.keyword_text + suffix + str(page * 30))
                    response.encoding = response.apparent_encoding
                    html = response.text
                    soup = BeautifulSoup(html, "html.parser")
                    # 找到所有图片标签
                    imgs = soup.find_all("img")
                    # 遍历图片标签，获取图片链接，下载图片并保存到指定文件夹
                    for img in imgs:
                        src = img.get("src")
                        if src:
                            if src.startswith("//"):
                                src = "http:" + src
                            elif src.startswith("/"):
                                src = self.url_text + src
                            elif src.startswith("data:image/svg+xml;utf8"): # 判断是否是svg格式
                                # 发送信号，更新爬取过程显示框
                                self.signal.emit(f"正在下载第{count+1}张图片：{src}")
                                #  下载图片并保存到指定文件夹，文件名为序号加".svg"后缀
                                urllib.request.urlretrieve(src, self.folder_text + f"/{count+1}.svg")
                                continue # 跳过后面的代码

                                
                            
                            # 判断是否包括动图，如果不包括则跳过gif格式的图片
                            if not self.gif_method and src.endswith(".gif"):
                                continue
                            # 发送信号，更新爬取过程显示框
                            self.signal.emit(f"正在下载第{count+1}张图片：{src}")
                            
                            # 下载图片并保存到指定文件夹，文件名为序号加后缀名
                            r = requests.get(src)
                            with open(self.folder_text + f"/{count+1}.{src.split('.')[-1]}", "wb") as f:
                                f.write(r.content)
                            # 更新计数器，如果达到指定数量则跳出循环
                            count += 1
                            if count == num:
                                break
                    if count == num:
                        break
                if count == num:
                    break
            # 发送信号，更新爬取过程显示框，显示爬取成功信息
            self.signal.emit(f"爬取成功，共下载了{count}张图片")
        except Exception as e:
            # 发送信号，更新爬取过程显示框，显示爬取失败信息和异常信息
            self.signal.emit(f"爬取失败，原因：{e}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("图片搜索下载应用")
        #self.resize(1800, 1200)
        self.mainlayout =QVBoxLayout()
        self.setLayout(self.mainlayout)


        # 创建网址方法勾选框，并设置状态改变时的槽函数
        self.webmethod_layout = QHBoxLayout()
        self.mainlayout.addLayout(self.webmethod_layout)
        self.url_check = QCheckBox("网址方法", self)
        #self.url_check.move(150, 150)
        self.webmethod_layout.addWidget(self.url_check)
        self.url_check.stateChanged.connect(self.url_check_changed)

        # 创建网址输入文本框，并设置为不可用状态
        self.url_edit = QLineEdit(self)
        #self.url_edit.move(450, 150)
        #self.url_edit.resize(1200, 75)
        self.webmethod_layout.addWidget(self.url_edit)
        self.url_edit.setPlaceholderText("请输入网址")
        self.url_edit.setEnabled(False)

        # 创建关键词方法勾选框，并设置状态改变时的槽函数
        self.keywordmethod_layout = QHBoxLayout()
        self.mainlayout.addLayout(self.keywordmethod_layout)
        self.keyword_check = QCheckBox("关键词方法", self)
        #self.keyword_check.move(150, 300)
        self.keywordmethod_layout.addWidget(self.keyword_check)
        self.keyword_check.stateChanged.connect(self.keyword_check_changed)

        # 创建关键词输入文本框，并设置为不可用状态
        self.keyword_edit = QLineEdit(self)
        #self.keyword_edit.move(150, 300)
        #self.keyword_edit.resize(600, 75)
        self.keywordmethod_layout.addWidget(self.keyword_edit)
        self.keyword_edit.setPlaceholderText("请输入关键词")
        self.keyword_edit.setEnabled(False)

        # 创建图片下载数量文本框，并设置为不可用状态
        self.num_edit = QLineEdit(self)
        #self.num_edit.move(1200, 300)
        #self.num_edit.resize(450, 75)
        self.keywordmethod_layout.addWidget(self.num_edit)
        self.num_edit.setPlaceholderText("请输入图片下载数量")
        self.num_edit.setEnabled(False)

        # 创建导出文件夹选择框，并设置点击时的槽函数
        self.folder_button = QPushButton("选择导出文件夹", self)
        #self.folder_button.move(500, 150)
        self.filechoice_layout = QHBoxLayout()
        self.mainlayout.addLayout(self.filechoice_layout)
        self.filechoice_layout.addWidget(self.folder_button)
        self.folder_button.clicked.connect(self.select_folder)

        # 创建导出文件夹显示标签，并设置为居中对齐和自动换行
        self.folder_label = QLabel(self)
        #self.folder_label.move(200, 150)
        #self.folder_label.resize(350, 25)
        self.filechoice_layout.addWidget(self.folder_label)
        self.folder_label.setAlignment(Qt.AlignCenter)
        self.folder_label.setWordWrap(True)

        # 创建是否包括动图勾选框，并设置默认为不选中状态
        self.gif_check = QCheckBox("是否包括动图",self)
        #self.gif_check.move(50, 200)
        self.checkgif_layout = QHBoxLayout()
        self.mainlayout.addLayout(self.checkgif_layout)
        self.checkgif_layout.addWidget(self.gif_check)
        self.gif_check.setChecked(False)

        # 创建启动按钮，并设置点击时的槽函数
        self.start_button = QPushButton("启动", self)
        #self.start_button.move(50, 250)
        self.checkgif_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_download)

        # 创建爬取过程显示框，并设置为只读状态
        self.process_edit = QTextEdit(self)
        #self.process_edit.move(150, 250)
        #self.process_edit.resize(400, 100)
        self.context_layout = QHBoxLayout()
        self.mainlayout.addLayout(self.context_layout)
        self.context_layout.addWidget(self.process_edit)
        self.process_edit.setMinimumSize(800,200)
        self.process_edit.setReadOnly(True)

        # 创建一个图片下载器对象，用来执行爬取逻辑
        self.downloader = ImageDownloader(False, "", False, "", "", "", False)
        # 连接图片下载器的信号和爬取过程显示框的槽函数，用来更新显示内容
        self.downloader.signal.connect(self.update_process)

    def url_check_changed(self):
        # 网址方法勾选框状态改变时的槽函数
        # 如果勾选了网址方法，则启用网址输入文本框，禁用关键词方法勾选框，关键词输入文本框和图片下载数量文本框
        if self.url_check.isChecked():
            self.url_edit.setEnabled(True)
            self.keyword_check.setEnabled(False)
            self.keyword_edit.setEnabled(False)
            self.num_edit.setEnabled(False)
        # 如果取消了网址方法，则禁用网址输入文本框，启用关键词方法勾选框
        else:
            self.url_edit.setEnabled(False)
            self.keyword_check.setEnabled(True)

    def keyword_check_changed(self):
        # 关键词方法勾选框状态改变时的槽函数
        # 如果勾选了关键词方法，则启用关键词输入文本框和图片下载数量文本框，禁用网址方法勾选框和网址输入文本框
        if self.keyword_check.isChecked():
            self.keyword_edit.setEnabled(True)
            self.num_edit.setEnabled(True)
            self.url_check.setEnabled(False)
            self.url_edit.setEnabled(False)
        # 如果取消了关键词方法，则禁用关键词输入文本框和图片下载数量文本框，启用网址方法勾选框
        else:
            self.keyword_edit.setEnabled(False)
            self.num_edit.setEnabled(False)
            self.url_check.setEnabled(True)

    def select_folder(self):
        # 导出文件夹选择框点击时的槽函数
        # 弹出一个文件对话框，让用户选择一个文件夹，并将其路径显示在导出文件夹显示标签上
        folder = QFileDialog.getExistingDirectory(self, "选择导出文件夹")
        if folder:
            self.folder_label.setText(folder)

    def start_download(self):
        # 启动按钮点击时的槽函数
        # 获取各个控件的状态和内容，并传递给图片下载器对象
        url_method = self.url_check.isChecked()
        url_text = self.url_edit.text()
        keyword_method = self.keyword_check.isChecked()
        keyword_text = self.keyword_edit.text()
        num_text = self.num_edit.text()
        folder_text = self.folder_label.text()
        gif_method = self.gif_check.isChecked()
        
        # 判断各项是否填写完整，如果不完整则弹出提示信息并返回
        if not (url_method or keyword_method):
            self.process_edit.setText("请选择一种方法")
            return
        if url_method and not url_text:
            self.process_edit.setText("请输入网址")
            return
        if keyword_method and not (keyword_text and num_text):
            self.process_edit.setText("请输入关键词和图片下载数量")
            return
        if not folder_text:
            self.process_edit.setText("请选择导出文件夹")
            return

        # 将各项参数传递给图片下载器对象，并启动线程开始爬取图片
        self.downloader.url_method = url_method
        self.downloader.url_text = url_text
        self.downloader.keyword_method = keyword_method
        self.downloader.keyword_text = keyword_text
        self.downloader.num_text = num_text
        self.downloader.folder_text = folder_text
        self.downloader.gif_method = gif_method

        # 清空爬取过程显示框，并显示开始爬取信息
        self.process_edit.clear()
        self.process_edit.setText("开始爬取图片")

        # 启动图片下载器线程
        self.downloader.start()

    def update_process(self, text):
        # 爬取过程显示框的槽函数，用来更新显示内容
        # 将图片下载器发来的信号（文本信息）追加到爬取过程显示框上
        self.process_edit.append(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
