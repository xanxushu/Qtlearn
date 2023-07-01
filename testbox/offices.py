 # 导入所需的模块
import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QFileDialog, QPushButton,QLabel, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QImage, QPixmap


# 定义一个自定义的窗口类，继承自QWidget
class ExcelViz(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # 调用初始化界面的方法

    def initUI(self):
        # 创建各种控件
        self.line_check = QCheckBox("折线图") # 选择输出图像的样式勾选框（折线图）
        self.bar_check = QCheckBox("柱状图") # 选择输出图像的样式勾选框（柱状图）
        self.image_label = QLabel() # 放置生成的图片的区域
        self.image_label.setAlignment(Qt.AlignCenter) # 设置图片居中显示
        self.file_edit = QLineEdit() # 文件选择的选择框，用来选择需要可视化的excel文件
        self.file_edit.setReadOnly(True) # 设置为只读，不允许用户输入
        self.file_button = QPushButton("选择文件") # 文件选择的按钮，用来打开文件对话框
        self.start_button = QPushButton("启动") # 启动按钮，用来开始生成图片
        self.x_edit = QLineEdit() # 横坐标设置文本框，用来选择excel文件中哪一列充当横坐标
        self.y_edit = QLineEdit() # 纵坐标设置文本框，用来选择excel文件中哪一列充当纵坐标
        self.start_row_edit = QLineEdit() # 起始行文本框，用来界定哪几行的数据需要被处理
        self.end_row_edit = QLineEdit() # 结束行文本框，用来界定哪几行的数据需要被处理
        self.cate_check = QCheckBox("是否分类") # 是否分类勾选框，勾选时，分类条件文本框才可用，用来输入分类条件
        self.cate_edit = QLineEdit() # 分类条件文本框，用来输入分类条件
        self.cate_edit.setEnabled(False) # 默认设置为不可用

        # 创建网格布局管理器，并将控件添加到相应的位置上
        grid = QGridLayout()
        grid.addWidget(self.line_check, 0, 0)
        grid.addWidget(self.bar_check, 0, 1)
        grid.addWidget(self.image_label, 1, 0, 1, 4)
        grid.addWidget(self.file_edit, 2, 0, 1, 3)
        grid.addWidget(self.file_button, 2, 3)
        grid.addWidget(self.start_button, 2, 4)
        grid.addWidget(QLabel("横坐标"), 3, 0)
        grid.addWidget(self.x_edit, 3, 1)
        grid.addWidget(QLabel("纵坐标"), 3, 2)
        grid.addWidget(self.y_edit, 3, 3)
        grid.addWidget(QLabel("起始行"), 4, 0)
        grid.addWidget(self.start_row_edit, 4, 1)
        grid.addWidget(QLabel("结束行"), 4, 2)
        grid.addWidget(self.end_row_edit, 4, 3)
        grid.addWidget(self.cate_check, 5, 0)
        grid.addWidget(self.cate_edit, 5 ,1)

        # 设置窗口的布局为网格布局
        self.setLayout(grid)

        # 连接信号和槽函数
        self.file_button.clicked.connect(self.select_file) # 点击文件选择按钮时，调用select_file方法
        self.start_button.clicked.connect(self.start_viz) # 点击启动按钮时，调用start_viz方法
        self.cate_check.stateChanged.connect(self.enable_cate_edit) # 分类勾选框状态改变时，调用enable_cate_edit方法

        # 设置窗口的标题和大小
        self.setWindowTitle("Excel数据可视化")
        self.resize(800, 600)

    def select_file(self):
        # 弹出文件对话框，选择excel文件，并将文件路径显示在文件选择框中
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel files (*.xlsx *.xls)")
        if file_name:
            self.file_edit.setText(file_name)

    def start_viz(self):
        # 获取用户输入的各种参数
        file_name = self.file_edit.text() # 文件路径
        x_col = self.x_edit.text() # 横坐标列名
        y_col = self.y_edit.text() # 纵坐标列名
        start_row = self.start_row_edit.text() # 起始行
        end_row = self.end_row_edit.text() # 结束行
        cate_col = self.cate_edit.text() if self.cate_check.isChecked() else None # 分类条件列名，如果分类勾选框没有勾选，则为None

        # 检查参数是否合法，如果不合法，则弹出错误提示框，并返回
        if not file_name:
            QMessageBox.critical(self, "错误", "请选择一个excel文件！")
            return
        if not x_col or not y_col:
            QMessageBox.critical(self, "错误", "请输入横纵坐标列名！")
            return
        if not start_row or not end_row:
            QMessageBox.critical(self, "错误", "请输入起始行和结束行！")
            return
        if not start_row.isdigit() or not end_row.isdigit():
            QMessageBox.critical(self, "错误", "起始行和结束行必须是数字！")
            return
        if self.cate_check.isChecked() and not cate_col:
            QMessageBox.critical(self, "错误", "请输入分类条件列名！")
            return

        # 尝试读取excel文件，并根据参数进行数据筛选和处理，如果出现异常，则弹出错误提示框，并返回
        try:
            df = pd.read_excel(file_name) # 读取excel文件，返回一个DataFrame对象
            df = df[[x_col, y_col] + ([cate_col] if cate_col else [])] # 选择需要的列
            df = df.iloc[int(start_row):int(end_row)] # 选择需要的行
            if cate_col: # 如果有分类条件，则按照分类条件分组
                grouped = df.groupby(cate_col)
            else: # 否则，将整个DataFrame作为一个分组
                grouped = [(None, df)]
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取或处理excel文件失败：{e}")
            return

        # 创建一个matplotlib的Figure对象，用来绘制图表
        fig = plt.figure()

        # 遍历每个分组，绘制相应的图表
        for i, (name, group) in enumerate(grouped):
            ax = fig.add_subplot(len(grouped), 1, i + 1) # 创建一个子图，位置为第i+1个
            if name: # 如果有分组名，则设置子图的标题为分组名
                ax.set_title(name)
            x_data = group[x_col] # 获取横坐标数据
            y_data = group[y_col] # 获取纵坐标数据
            if self.line_check.isChecked(): # 如果用户选择了折线图，则绘制折线图
                ax.plot(x_data, y_data)
            if self.bar_check.isChecked(): # 如果用户选择了柱状图，则绘制柱状图
                ax.bar(x_data, y_data)
            ax.set_xlabel(x_col) # 设置横坐标标签为横坐标列名
            ax.set_ylabel(y_col) # 设置纵坐标标签为纵坐标列名

        # 调整子图之间的间距，并将Figure对象转换为QPixmap对象，显示在图片区域中
        fig.tight_layout()
        fig.canvas.draw()
        image = fig.canvas.buffer_rgba() # 获取Figure对象的RGBA缓冲区
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGBA8888) # 将缓冲区转换为QImage对象
        pixmap = QPixmap.fromImage(qimage) # 将QImage对象转换为QPixmap对象
        self.image_label.setPixmap(pixmap) # 将QPixmap对象显示在图片区域中

    def enable_cate_edit(self):
        # 根据分类勾选框的状态，设置分类条件文本框的可用性
        if self.cate_check.isChecked():
            self.cate_edit.setEnabled(True)
        else:
            self.cate_edit.setEnabled(False)

# 创建应用对象，创建窗口对象，显示窗口，进入事件循环
if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = ExcelViz()
    window.show()
    sys.exit(app.exec_())