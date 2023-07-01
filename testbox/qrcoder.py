from PyQt5 import QtWidgets,QtGui
import qrcode
import io
import traceback
import datetime

class QrcodeApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(450,220)
        self.setWindowTitle("二维码生成器")
        self.main_layout = QtWidgets.QGridLayout() # 窗口网格布局
        self.label_desc = QtWidgets.QLabel("输入文字或网址：")
        self.input_content = QtWidgets.QLineEdit() # 二维码内容
        self.lable_size = QtWidgets.QLabel("图片尺寸：")
        self.label_space = QtWidgets.QLabel("留白设置：")
        self.lable_pre = QtWidgets.QLabel("预览：")
        self.input_size = QtWidgets.QComboBox() # 二维码编码类型
        self.input_size.addItem("210*210")
        self.input_size.addItem("420*420")
        self.input_size.addItem("630*630")
        self.input_space = QtWidgets.QSpinBox() # 二维码留白大小
        self.save_qrcode = QtWidgets.QPushButton("保存二维码")
        self.qrcode_img = QtWidgets.QLabel()
        self.qrcode_img.setScaledContents(True) # 设置二维码图像容器内部件缩放
        self.qrcode_img.setMinimumSize(190,190) # 固定二维码图像容器大小

        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label_desc,0,0,1,2)
        self.main_layout.addWidget(self.input_content, 1, 0, 1, 2)
        self.main_layout.addWidget(self.lable_size, 2, 0, 1, 1)
        self.main_layout.addWidget(self.label_space, 2, 1, 1, 1)
        self.main_layout.addWidget(self.input_size, 3, 0, 1, 1)
        self.main_layout.addWidget(self.input_space, 3, 1, 1, 1)
        self.main_layout.addWidget(self.save_qrcode,4,0,1,2)
        self.main_layout.addWidget(self.lable_pre,0,2,)
        self.main_layout.addWidget(self.qrcode_img, 1, 2, 5, 2)

        # 绑定信号槽函数
        self.input_content.textChanged.connect(self.value_change) # 输入内容改变时触发
        self.input_size.currentTextChanged.connect(self.value_change) # 图片尺寸改变时触发
        self.input_space.valueChanged.connect(self.value_change) # 留白大小改变时触发
        self.save_qrcode.clicked.connect(self.save_image) # 点击保存按钮时触发

    def value_change(self):
        try:
            qr_text = self.input_content.text() # 二维码内容值
            qr_size = int(self.input_size.currentText().split("*")[0]) # 二维码图片尺寸值
            qr_space = self.input_space.value() # 二维码留白大小值
            qr_img = qrcode.make(qr_text,box_size=qr_size,border=qr_space) # 生成二维码图片对象
            img_bytes = io.BytesIO() # 创建字节流对象
            qr_img.save(img_bytes,format="PNG") # 将二维码图片保存到字节流中
            qt_img = QtGui.QImage.fromData(img_bytes.getvalue()) # 将字节流转换为QImage对象
            self.qrcode_img.setPixmap(QtGui.QPixmap.fromImage(qt_img)) # 将QImage对象设置为标签的图像
        except Exception as e:
            traceback.print_exc()

    def save_image(self):
        try:
            img_bytes = io.BytesIO() # 创建字节流对象
            self.qrcode_img.pixmap().save(img_bytes,format="PNG") # 将标签的图像保存到字节流中
            file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png" # 以当前时间为文件名
            with open(file_name,"wb") as f: # 以二进制写入模式打开文件
                f.write(img_bytes.getvalue()) # 将字节流写入文件中
                QtWidgets.QMessageBox.information(self,"提示","保存成功！")
        except Exception as e:
            traceback.print_exc()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = QrcodeApp()
    win.show()
    app.exec_()
