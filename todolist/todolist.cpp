// todolist.cpp
#include "todolist.h"
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QMessageBox>
#include <QDate>
#include <algorithm>

// TodoItem类的构造函数，用来初始化todo项目的各项属性
TodoItem::TodoItem(int flag,const QString &title, const QDateTime &start, const QDateTime &end, const QString &note, const QString &group,QListWidget *parent)
    : QListWidgetItem(parent), title(title), start(start), end(end), note(note), group(group)
{
    // 设置todo项目的显示文本，包括勾选框和todo项目的内容，起止时间，今天据截止日期的剩余天数
    if(flag==0){
    setText(QString("[ ] %1 (%2 - %3) %4天").arg(title).arg(start.toString("yyyy-MM-dd")).arg(end.toString("yyyy-MM-dd")).arg(QDate::currentDate().daysTo(end.date())));
    }
    else{
        setText(QString("[x] %1 (%2 - %3) %4天").arg(title).arg(start.toString("yyyy-MM-dd")).arg(end.toString("yyyy-MM-dd")).arg(QDate::currentDate().daysTo(end.date())));
    }
}

// TodoItem类的析构函数，暂时不需要做任何事情
TodoItem::~TodoItem()
{

}

// 获取todo项目的标题
QString TodoItem::getTitle() const
{
    return title;
}

// 设置todo项目的标题，并更新显示文本
void TodoItem::setTitle(const QString &title)
{
    this->title = title;
    setText(QString("[ ] %1 (%2 - %3) %4天").arg(title).arg(start.toString("yyyy-MM-dd")).arg(end.toString("yyyy-MM-dd")).arg(QDate::currentDate().daysTo(end.date())));
}

// 获取todo项目的起始时间
QDateTime TodoItem::getStart() const
{
    return start;
}

// 设置todo项目的起始时间，并更新显示文本
void TodoItem::setStart(const QDateTime &start)
{
    this->start = start;
    setText(QString("[ ] %1 (%2 - %3) %4天").arg(title).arg(start.toString("yyyy-MM-dd")).arg(end.toString("yyyy-MM-dd")).arg(QDate::currentDate().daysTo(end.date())));
}

// 获取todo项目的截止时间
QDateTime TodoItem::getEnd() const
{
    return end;
}

// 设置todo项目的截止时间，并更新显示文本
void TodoItem::setEnd(const QDateTime &end)
{
    this->end = end;
    setText(QString("[ ] %1 (%2 - %3) %4天").arg(title).arg(start.toString("yyyy-MM-dd")).arg(end.toString("yyyy-MM-dd")).arg(QDate::currentDate().daysTo(end.date())));
}

// 获取todo项目的备注
QString TodoItem::getNote() const
{
    return note;
}

// 设置todo项目的备注
void TodoItem::setNote(const QString &note)
{
    this->note = note;
}

// 获取todo项目的分组
QString TodoItem::getGroup() const
{
    return group;
}

// 设置todo项目的分组
void TodoItem::setGroup(const QString &group)
{
    this->group = group;
}

// EditDialog类的构造函数，用来初始化对话框中的各个控件，并连接信号和槽函数
EditDialog::EditDialog(TodoItem *item, QWidget *parent)
    : QDialog(parent), item(item)
{
    // 创建各个控件，并设置一些属性，如最小宽度，格式等
    titleLabel = new QLabel(tr("标题："), this);
    titleEdit = new QLineEdit(this);
    titleEdit->setMinimumWidth(300);
    titleEdit->setText(item->getTitle());

    startLabel = new QLabel(tr("起始时间："), this);
    startEdit = new QDateTimeEdit(this);
    startEdit->setDisplayFormat("yyyy-MM-dd hh:mm");
    startEdit->setDateTime(item->getStart());

    endLabel = new QLabel(tr("截止时间："), this);
    endEdit = new QDateTimeEdit(this);
    endEdit->setDisplayFormat("yyyy-MM-dd hh:mm");
    endEdit->setDateTime(item->getEnd());

    noteLabel = new QLabel(tr("备注："), this);
    noteEdit = new QTextEdit(this);
    noteEdit->setText(item->getNote());

    groupLabel = new QLabel(tr("分组："), this);
    groupEdit = new QLineEdit(this);
    groupEdit->setText(item->getGroup());

    saveButton = new QPushButton(tr("保存"), this);
    cancelButton = new QPushButton(tr("取消"), this);

    // 连接信号和槽函数，用来响应用户的操作
    connect(saveButton, &QPushButton::clicked, this, &EditDialog::save);
    connect(cancelButton, &QPushButton::clicked, this, &EditDialog::cancel);

    // 使用布局管理器来排列各个控件的位置
    QHBoxLayout *titleLayout = new QHBoxLayout;
    titleLayout->addWidget(titleLabel);
    titleLayout->addWidget(titleEdit);

    QHBoxLayout *startLayout = new QHBoxLayout;
    startLayout->addWidget(startLabel);
    startLayout->addWidget(startEdit);

    QHBoxLayout *endLayout = new QHBoxLayout;
    endLayout->addWidget(endLabel);
    endLayout->addWidget(endEdit);

    QHBoxLayout *noteLayout = new QHBoxLayout;
    noteLayout->addWidget(noteLabel);
    noteLayout->addWidget(noteEdit);

    QHBoxLayout *groupLayout = new QHBoxLayout;
    groupLayout->addWidget(groupLabel);
    groupLayout->addWidget(groupEdit);

    QHBoxLayout *buttonLayout = new QHBoxLayout;
    buttonLayout->addStretch();
    buttonLayout->addWidget(saveButton);
    buttonLayout->addWidget(cancelButton);

    QVBoxLayout *mainLayout = new QVBoxLayout;
    mainLayout->addLayout(titleLayout);
    mainLayout->addLayout(startLayout);
    mainLayout->addLayout(endLayout);
    mainLayout->addLayout(noteLayout);
    mainLayout->addLayout(groupLayout);
    mainLayout->addStretch();
    mainLayout->addLayout(buttonLayout);

    setLayout(mainLayout); // 设置对话框的布局
}

// EditDialog类的析构函数，暂时不需要做任何事情
EditDialog::~EditDialog()
{

}

// 保存编辑内容的槽函数，用来将编辑框中的内容更新到todo项目中，并关闭对话框
void EditDialog::save()
{
    // 获取编辑框中的内容，并检查是否合法，如标题不能为空，截止时间不能早于起始时间等
    QString title = titleEdit->text().trimmed();
    QDateTime start = startEdit->dateTime();
    QDateTime end = endEdit->dateTime();
    QString note = noteEdit->toPlainText().trimmed();
    QString group = groupEdit->text().trimmed();

    if (title.isEmpty()) {
        QMessageBox::warning(this, tr("警告"), tr("标题不能为空！"));
        return;
    }

    if (end < start) {
        QMessageBox::warning(this, tr("警告"), tr("截止时间不能早于起始时间！"));
        return;
    }

    // 将编辑框中的内容更新到todo项目中
    item->setTitle(title);
    item->setStart(start);
    item->setEnd(end);
    item->setNote(note);
    item->setGroup(group);

    accept(); // 关闭对话框，并返回QDialog::Accepted
}

// 取消编辑的槽函数，用来关闭对话框，不做任何修改
void EditDialog::cancel()
{
   reject(); // 关闭对话框，并返回QDialog::Rejected
}

// TodoList类的构造函数，用来初始化主窗口中的各个控件，并连接信号和槽函数
TodoList::TodoList(QWidget *parent)
     : QMainWindow(parent)
{

     // 创建各个控件，并设置一些属性，如最小宽度，最小高度等
     groupList = new QListWidget(this); // 分组列表
     groupList->setMinimumWidth(60);
     groupList->setMaximumWidth(100);

     todoList = new QListWidget(this); // todo列表
     todoList->setMinimumHeight(300);

     sortCheck = new QCheckBox(tr("按剩余天数排序"), this); // 排序复选框

     addButton = new QPushButton(tr("添加"), this); // 添加按钮
     removeButton = new QPushButton(tr("删除"), this); // 删除按钮
     setContextMenuPolicy(Qt::CustomContextMenu);//右击事件

     // 连接信号和槽函数，用来响应用户的操作
     connect(addButton, &QPushButton::clicked, this, &TodoList::add); // 点击添加按钮时，调用add()函数
     connect(removeButton, &QPushButton::clicked, this, &TodoList::remove); // 点击删除按钮时，调用remove()函数
     connect(todoList, &QListWidget::itemDoubleClicked, this, &TodoList::edit); // 双击todo列表中的项目时，调用edit()函数
     connect(groupList, &QListWidget::itemClicked, this, &TodoList::filter); // 点击分组列表中的项目时，调用filter()函数
     connect(sortCheck, &QCheckBox::stateChanged, this, &TodoList::sort); // 改变排序复选框的状态时，调用sort()函数
     connect(this, &TodoList::customContextMenuRequested, this, &TodoList::done);

     // 使用布局管理器来排列各个控件的位置
     QHBoxLayout *buttonLayout = new QHBoxLayout;
     buttonLayout->addWidget(addButton);
     buttonLayout->addWidget(removeButton);

     QVBoxLayout *todoLayout = new QVBoxLayout;
     todoLayout->addWidget(todoList);
     todoLayout->addWidget(sortCheck);
     todoLayout->addLayout(buttonLayout);

     QHBoxLayout *mainLayout = new QHBoxLayout;
     mainLayout->addWidget(groupList);
     mainLayout->addLayout(todoLayout);

     QWidget *widget = new QWidget(this); // 创建一个中心窗口部件，用来承载布局
     widget->setLayout(mainLayout); // 设置中心窗口部件的布局
     setCentralWidget(widget); // 设置主窗口的中心窗口部件
     load("todolist.dat");
     updateGroupList(); // 更新分组列表的内容和显示

     setWindowTitle(tr("TodoList")); // 设置主窗口的标题
     setWindowIcon(QIcon(":/xanxushu.ico"));

}

// TodoList类的析构函数，暂时不需要做任何事情
TodoList::~TodoList()
{
    save("todolist.dat");

}

// 添加todo项目的槽函数，用来弹出一个编辑对话框，让用户输入新的todo项目的内容，并添加到todo列表中
void TodoList::add()
{
    // 创建一个新的todo项目，初始属性为空或默认值
    TodoItem *item = new TodoItem(0,"", QDateTime::currentDateTime(), QDateTime::currentDateTime().addDays(1), "", "全部", todoList);

    // 创建一个编辑对话框，传入新建的todo项目
    EditDialog *dialog = new EditDialog(item, this);

    // 显示对话框，并等待用户操作
    int result = dialog->exec();

    // 如果用户点击了保存按钮，则将新建的todo项目添加到todo列表中，并更新分组列表
    if (result == QDialog::Accepted) {
        todoList->addItem(item);
        updateGroupList();
    }
    // 如果用户点击了取消按钮，则删除新建的todo项目，不做任何修改
    else {
        delete item;
    }

    delete dialog; // 删除对话框
}

// 删除todo项目的槽函数，用来删除todo列表中选中的项目，并更新分组列表
void TodoList::remove()
{
    // 获取todo列表中选中的项目，如果没有选中任何项目，则返回
    QList<QListWidgetItem *> items = todoList->selectedItems();
    if (items.isEmpty()) {
        return;
    }

    // 弹出一个确认对话框，询问用户是否确定要删除选中的项目
    int result = QMessageBox::question(this, tr("确认"), tr("确定要删除选中的项目吗？"));

    // 如果用户点击了是按钮，则遍历选中的项目，并从todo列表中删除它们
    if (result == QMessageBox::Yes) {
        for (QListWidgetItem *item : items) {
            delete item;
        }
        updateGroupList(); // 更新分组列表
    }
}

// 编辑todo项目的槽函数，用来弹出一个编辑对话框，让用户修改选中的todo项目的内容，并更新到todo列表中
void TodoList::edit(QListWidgetItem *item)
{
    // 将参数item转换为TodoItem类型，并检查是否为空指针，如果为空，则返回
    TodoItem *todoItem = dynamic_cast<TodoItem *>(item);
    if (!todoItem) {
        return;
    }

    // 创建一个编辑对话框，传入要编辑的todo项目
    EditDialog *dialog = new EditDialog(todoItem, this);

    // 显示对话框，并等待用户操作
    int result = dialog->exec();

    // 如果用户点击了保存按钮，则更新分组列表
    if (result == QDialog::Accepted) {
        updateGroupList();
    }

    delete dialog; // 删除对话框
}

// 根据分组筛选todo项目的槽函数，用来显示或隐藏todo列表中的项目，使之与选中的分组相匹配
void TodoList::filter(QListWidgetItem *item)
{
    // 获取分组列表中选中的项目的文本，如果没有选中任何项目，则返回
    QString group = item->text();
    if (group.isEmpty()) {
        return;
    }

    // 遍历todo列表中的所有项目，将它们转换为TodoItem类型，并检查是否为空指针
    for (int i = 0; i < todoList->count(); i++) {
        TodoItem *todoItem = dynamic_cast<TodoItem *>(todoList->item(i));
        if (!todoItem) {
            continue;
        }

        // 如果todo项目未勾选，并且其分组与选中的分组相同，或者选中的分组是"全部"，则显示该项目，否则隐藏该项目
                if (!todoItem->text().startsWith("[x]") && (todoItem->getGroup() == group || group == "全部")) {
                    todoItem->setHidden(false);
                }
                else if (todoItem->text().startsWith("[x]")&& (todoItem->getGroup() == group )) {
                    todoItem->setHidden(false);
                }
                else {
                    todoItem->setHidden(true);
                }
    }
}

// 根据剩余天数排序todo项目的槽函数，用来按照截止日期与当前日期的差值对todo列表中的项目进行升序或降序排序
void TodoList::sort(int state)
{
    // 定义一个比较函数，用来比较两个todo项目的剩余天数
    auto compare = [](const QListWidgetItem *item1, const QListWidgetItem *item2) {
        // 将参数item1和item2转换为TodoItem类型，并检查是否为空指针
        const TodoItem *todoItem1 = dynamic_cast<const TodoItem *>(item1);
        const TodoItem *todoItem2 = dynamic_cast<const TodoItem *>(item2);
        if (!todoItem1 || !todoItem2) {
            return false;
        }

        // 返回两个todo项目的截止日期与当前日期的差值的比较结果
        // 如果两个todo项目都未勾选，则按照剩余天数排序
                if (!todoItem1->text().startsWith("[x]") && !todoItem2->text().startsWith("[x]")) {
                    return QDate::currentDate().daysTo(todoItem1->getEnd().date()) < QDate::currentDate().daysTo(todoItem2->getEnd().date());
                }
                // 如果两个todo项目都已勾选，则按照默认顺序排序
                else if (todoItem1->text().startsWith("[x]") && todoItem2->text().startsWith("[x]")) {
                    return false;
                }
                // 如果一个todo项目未勾选，另一个已勾选，则优先显示未勾选的项目
                else {
                    return !todoItem1->text().startsWith("[x]");
                }
    };

    // 如果排序复选框被勾选，则按照升序排序todo列表中的项目，否则按照默认顺序排序
    if (state == Qt::Checked) {
        todoList->sortItems(Qt::AscendingOrder);
    }
    else {
        todoList->sortItems(Qt::DescendingOrder);
    }
}

void TodoList::done()
{
    // 获取todo列表中选中的项目，如果没有选中任何项目，则返回
    QList<QListWidgetItem *> items = todoList->selectedItems();
    if (items.isEmpty()) {
        return;
    }

    // 遍历选中的项目，并将它们转换为TodoItem类型，并检查是否为空指针
    for (QListWidgetItem *item : items) {
        TodoItem *todoItem = dynamic_cast<TodoItem *>(item);
        if (!todoItem) {
            continue;
        }

        // 将todo项目的分组设置为"已完成"，并在显示文本前面加上"[x]"表示已勾选
        todoItem->setGroup("已完成");
        todoItem->setText("[x]" + todoItem->text().mid(3));
    }
    updateGroupList(); // 更新分组列表
}

void TodoList::mousePressEvent(QMouseEvent *event)
{
    // 调用父类的mousePressEvent()函数，处理其他鼠标事件
    QMainWindow::mousePressEvent(event);

    // 如果鼠标右键被点击，则调用complete()函数
    if (event->button() == Qt::RightButton) {
        done();
    }
}

// 更新分组列表的内容和显示的函数，用来根据todo列表中的项目的分组情况，更新分组列表中的项目，并保持选中状态不变
void TodoList::updateGroupList()
{
    // 获取分组列表中当前选中的项目的文本，如果没有选中任何项目，则默认为"全部"
    QString currentGroup = groupList->currentItem() ? groupList->currentItem()->text() : "全部";

    // 清空分组列表中的所有项目
    groupList->clear();

    // 创建一个字符串列表，用来存储所有出现过的分组名称，并添加"全部"作为第一个元素
    QStringList groups;
    groups << "全部";

    // 遍历todo列表中的所有项目，将它们转换为TodoItem类型，并检查是否为空指针
    for (int i = 0; i < todoList->count(); i++) {
        TodoItem *todoItem = dynamic_cast<TodoItem *>(todoList->item(i));
        if (!todoItem) {
            continue;
        }

        // 获取todo项目的分组名称，如果该名称不在字符串列表中，则将其添加到字符串列表中
        QString group = todoItem->getGroup();
        if (!groups.contains(group)) {
            groups << group;
        }
    }

    // 遍历字符串列表中的所有元素，并将它们作为新的项目添加到分组列表中
    for (const QString &group : groups) {
        QListWidgetItem *item = new QListWidgetItem(group, groupList);
        if (group == currentGroup) {
                    item->setSelected(true);
                }
            }
        }

// 保存todo列表中的数据到文件的函数，传入一个文件名作为参数
void TodoList::save(const QString &fileName)
{
    // 创建一个QSaveFile对象，用来写入文件
    QSaveFile file(fileName);

    // 以只写和二进制模式打开文件，如果打开失败，则返回
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        return;
    }

    // 创建一个QDataStream对象，用来序列化数据
    QDataStream out(&file);

    // 设置数据流的版本号和字节顺序
    out.setVersion(QDataStream::Qt_5_14);
    out.setByteOrder(QDataStream::LittleEndian);

    // 遍历todo列表中的所有项目，将它们转换为TodoItem类型，并检查是否为空指针
    for (int i = 0; i < todoList->count(); i++) {
        TodoItem *todoItem = dynamic_cast<TodoItem *>(todoList->item(i));
        if (!todoItem) {
            continue;
        }

        // 将todo项目的各个属性写入数据流中
        // 将todo项目的各个属性写入数据流中
        // 如果todo项目的text属性以"[x]"或"[ ]"开头，则将前面的四个字符单独写入数据流中，作为一个标记
        QString text = todoItem->text();
        bool checked = false;
        if (text.startsWith("[x]")) {
            checked = true;
            text = text.mid(4);
        }
        else if (text.startsWith("[ ]")) {
            text = text.mid(4);
        }
        out << checked;
        out << todoItem->getTitle();
        out << todoItem->getStart();
        out << todoItem->getEnd();
        out << todoItem->getNote();
        out << todoItem->getGroup();

    }

    // 提交写入操作，如果失败，则返回
    if (!file.commit()) {
        return;
    }
}

// 从文件中加载数据到todo列表中的函数，传入一个文件名作为参数
void TodoList::load(const QString &fileName)
{
    // 创建一个QFile对象，用来读取文件
    QFile file(fileName);

    // 以只读和二进制模式打开文件，如果打开失败，则返回
    if (!file.open(QIODevice::ReadOnly)) {
        return;
    }

    // 创建一个QDataStream对象，用来反序列化数据
    QDataStream in(&file);

    // 设置数据流的版本号和字节顺序
    in.setVersion(QDataStream::Qt_5_14);
    in.setByteOrder(QDataStream::LittleEndian);

    // 清空todo列表中的所有项目
    todoList->clear();

    // 循环读取数据流中的数据，直到到达末尾
    while (!in.atEnd()) {
        // 声明一些变量，用来存储读取出来的todo项目的属性
        QString title;
        QDateTime start;
        QDateTime end;
        QString note;
        QString group;

        // 从数据流中读取todo项目的各个属性，并赋值给变量
        bool checked;
        in >> checked;
        in >> title;
        in >> start;
        in >> end;
        in >> note;
        in >> group;

        int flag = 0;

        // 根据读取出来的标记，给text属性添加前缀"[x]"或"[ ]"
        if (checked) {
            flag=1;
        }
        else {
            flag=0;
        }

        // 创建一个新的todo项目，并设置其各个属性
        TodoItem *item = new TodoItem(flag,title, start, end, note, group, todoList);
        // 将新建的todo项目添加到todo列表中
        todoList->addItem(item);
    }

    // 更新分组列表的内容和显示
    updateGroupList();
}

