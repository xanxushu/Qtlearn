// main.cpp
#include "todolist.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv); // 创建一个QApplication对象，用来管理应用程序的资源和事件循环

    TodoList todoList; // 创建一个TodoList对象，用来表示主窗口
    todoList.show(); // 显示主窗口

    return app.exec(); // 进入事件循环，等待用户操作
}
