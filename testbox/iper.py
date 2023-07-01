import sys
from PyQt5 import QtCore, QtNetwork, QtWidgets
import requests

class IPQueryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个文本框，用来输入要查询的ip地址
        self.ip_input = QtWidgets.QLineEdit()
        # 创建一个按钮，用来触发查询操作
        self.query_button = QtWidgets.QPushButton("查询")
        # 创建一个标签，用来显示当前IP地址
        self.current_ip_label = QtWidgets.QLabel()
        # 创建一个标签，用来显示IP地址的归属地
        self.location_label = QtWidgets.QLabel()
        # 创建一个标签，用来显示IP地址的网络
        self.network_label = QtWidgets.QLabel()
        # 创建一个标签，用来显示IP地址的经纬度
        self.coordinates_label = QtWidgets.QLabel()
        # 创建一个布局管理器，用来排列控件
        self.layout = QtWidgets.QVBoxLayout()
        # 将控件添加到布局管理器中
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.query_button)
        self.layout.addWidget(self.current_ip_label)
        self.layout.addWidget(self.location_label)
        self.layout.addWidget(self.network_label)
        self.layout.addWidget(self.coordinates_label)
        # 设置窗口的布局为布局管理器
        self.setLayout(self.layout)
        # 设置窗口的标题
        self.setWindowTitle("IP地址查询")
        # 连接按钮的点击信号到查询槽函数
        self.query_button.clicked.connect(self.query)
        # 获取当前用户的IP地址并解析显示
        self.get_current_ip()
    
    def get_current_ip(self):
        # 使用requests库发送一个GET请求到ipinfo.io网站，获取当前用户的IP地址和相关信息
        response = requests.get("https://ipinfo.io")
        # 如果请求成功，解析返回的JSON数据
        if response.status_code == 200:
            data = response.json()
            # 获取IP地址、归属地、网络和经纬度，并显示在对应的标签上
            ip = data["ip"]
            location = data["city"] + ", " + data["region"] + ", " + data["country"]
            network = data["org"]
            coordinates = data["loc"]
            self.current_ip_label.setText(f"当前IP地址：{ip}")
            self.location_label.setText(f"归属地：{location}")
            self.network_label.setText(f"网络：{network}")
            self.coordinates_label.setText(f"经纬度：{coordinates}")
    
    def query(self):
        # 获取文本框中输入的内容
        ip = self.ip_input.text()
        # 如果输入不为空，使用QHostAddress类来解析输入的IP地址内容
        if ip:
            address = QtNetwork.QHostAddress(ip)
            # 如果解析成功，使用requests库发送一个GET请求到ipinfo.io网站，获取输入的IP地址和相关信息
            if not address.isNull():
                response = requests.get(f"https://ipinfo.io/{ip}")
                # 如果请求成功，解析返回的JSON数据
                if response.status_code == 200:
                    data = response.json()
                    # 获取IP地址、归属地、网络和经纬度，并显示在对应的标签上
                    ip = data["ip"]
                    location = data["city"] + ", " + data["region"] + ", " + data["country"]
                    network = data["org"]
                    coordinates = data["loc"]
                    self.current_ip_label.setText(f"当前IP地址：{ip}")
                    self.location_label.setText(f"归属地：{location}")
                    self.network_label.setText(f"网络：{network}")
                    self.coordinates_label.setText(f"经纬度：{coordinates}")
                else:
                    # 如果请求失败，显示一个错误信息
                    QtWidgets.QMessageBox.critical(self, "错误", "无法获取IP地址信息")
            else:
                # 如果解析失败，显示一个错误信息
                QtWidgets.QMessageBox.critical(self, "错误", "无效的IP地址格式")
        else:
            # 如果输入为空，显示一个错误信息
            QtWidgets.QMessageBox.critical(self, "错误", "请输入要查询的IP地址")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ip_query_app = IPQueryApp()
    ip_query_app.show()
    sys.exit(app.exec_())
