# todolist.pro
QT       += core gui # 使用Qt的核心和图形模块

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets # 如果Qt的主版本号大于4，则使用Qt的窗口部件模块

CONFIG += c++11 # 使用C++11标准

TARGET = newproject # 设置项目的目标名称
TEMPLATE = app # 设置项目的模板类型为应用程序

# 设置项目的源文件
SOURCES += \
        main.cpp \
        todolist.cpp

# 设置项目的头文件
HEADERS += \
        todolist.h

# 设置项目的库文件
#LIBS += -lQt5Widgets -lQt5Gui -lQt5Core

RESOURCES += \
    needs.qrc
