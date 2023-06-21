// todolist.h
#ifndef TODOLIST_H
#define TODOLIST_H

#include <QMainWindow>
#include <QListWidget>
#include <QListWidgetItem>
#include <QCheckBox>
#include <QPushButton>
#include <QLabel>
#include <QDateTimeEdit>
#include <QLineEdit>
#include <QTextEdit>
#include <QDialog>
#include <QMouseEvent>
#include <QSaveFile>
#include <QDataStream>
// 定义一个TodoItem类，继承自QListWidgetItem，用来表示每个todo项目
class TodoItem : public QListWidgetItem
{
public:
    TodoItem(int flag,const QString &title, const QDateTime &start, const QDateTime &end, const QString &note, const QString &group, QListWidget *parent = nullptr);
    ~TodoItem();

    // 获取或设置todo项目的各项属性
    QString getTitle() const;
    void setTitle(const QString &title);

    QDateTime getStart() const;
    void setStart(const QDateTime &start);

    QDateTime getEnd() const;
    void setEnd(const QDateTime &end);

    QString getNote() const;
    void setNote(const QString &note);

    QString getGroup() const;
    void setGroup(const QString &group);

private:
    // 用私有成员变量来存储todo项目的各项属性
    QString title;
    QDateTime start;
    QDateTime end;
    QString note;
    QString group;
};

// 定义一个EditDialog类，继承自QDialog，用来表示编辑todo项目的对话框
class EditDialog : public QDialog
{
    Q_OBJECT

public:
    EditDialog(TodoItem *item, QWidget *parent = nullptr);
    ~EditDialog();

private slots:
    // 定义槽函数，用来响应用户的操作
    void save(); // 保存编辑内容
    void cancel(); // 取消编辑

private:
    // 定义私有成员变量，用来表示对话框中的各个控件
    TodoItem *item; // 指向要编辑的todo项目
    QLabel *titleLabel; // 标题标签
    QLineEdit *titleEdit; // 标题编辑框
    QLabel *startLabel; // 起始时间标签
    QDateTimeEdit *startEdit; // 起始时间编辑框
    QLabel *endLabel; // 截止时间标签
    QDateTimeEdit *endEdit; // 截止时间编辑框
    QLabel *noteLabel; // 备注标签
    QTextEdit *noteEdit; // 备注编辑框
    QLabel *groupLabel; // 分组标签
    QLineEdit *groupEdit; // 分组编辑框
    QPushButton *saveButton; // 保存按钮
    QPushButton *cancelButton; // 取消按钮
};

// 定义一个TodoList类，继承自QMainWindow，用来表示主窗口
class TodoList : public QMainWindow
{
    Q_OBJECT

public:
    TodoList(QWidget *parent = nullptr);
    ~TodoList();
    void save(const QString &fileName);
    void load(const QString &fileName);

private slots:
     // 定义槽函数，用来响应用户的操作
     void add(); // 添加todo项目
     void remove(); // 删除todo项目
     void edit(QListWidgetItem *item); // 编辑todo项目
     void filter(QListWidgetItem *item); // 根据分组筛选todo项目
     void sort(int state); // 根据剩余天数排序todo项目
     void done();//将该todo项目设置为已完成

protected:
     void mousePressEvent(QMouseEvent *event) override;

private:
     // 定义私有成员变量，用来表示主窗口中的各个控件
     QListWidget *groupList; // 分组列表
     QListWidget *todoList; // todo列表
     QCheckBox *sortCheck; // 排序复选框
     QPushButton *addButton; // 添加按钮
     QPushButton *removeButton; // 删除按钮

     void updateGroupList(); // 更新分组列表的内容和显示

};

#endif // TODOLIST_H

