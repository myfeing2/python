import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QSizePolicy,
    QLineEdit, QSpinBox
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTabWidget 自适应布局示例")
        # 初始窗口大小，可自由拖拽缩放
        self.resize(800, 600)

        # 1. 创建中心部件和主布局（必须给中心部件加布局，控件才会随窗口缩放）
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置边距
        main_layout.setSpacing(10)  # 控件间距

        # 2. 创建QTabWidget，设置尺寸策略为可扩展，占满可用空间
        self.tab_widget = QTabWidget()
        # 核心：让TabWidget在水平和垂直方向都随布局拉伸
        self.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        # 设置Tab位置为顶部（默认就是顶部，可改成West/Left放左边等）
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        # 设置Tab可以关闭（如果不需要可以删掉这行）
        # self.tab_widget.setTabsClosable(True)

        # 3. 设置Tab标签栏的尺寸样式
        self.tab_widget.tabBar().setStyleSheet("""
            QTabBar::tab {
                min-width: 120px;   /* 标签最小宽度 */
                max-width: 200px;   /* 标签最大宽度，防止文字过长拉太宽 */
                min-height: 32px;   /* 标签高度 */
                padding: 5px 15px;  /* 文字内边距 */
                font-size: 14px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #f0f0f0;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #e8e8e8;
            }
        """)

        # 4. 添加第一个Tab页：文本编辑页
        self.add_text_edit_tab()
        # 5. 添加第二个Tab页：表单设置页
        self.add_form_tab()

        # 把TabWidget加到主布局里
        main_layout.addWidget(self.tab_widget)

        # 底部加个示例按钮，不影响TabWidget的拉伸
        bottom_btn = QPushButton("底部测试按钮")
        bottom_btn.setFixedHeight(35)
        main_layout.addWidget(bottom_btn)

    def add_text_edit_tab(self):
        """第一个Tab：文本编辑页，内容自动撑满"""
        tab1 = QWidget()
        # 核心：每个Tab页必须自己加布局，内部控件才会随Tab缩放
        tab_layout = QVBoxLayout(tab1)
        tab_layout.setContentsMargins(15, 15, 15, 15)
        tab_layout.setSpacing(10)

        # 顶部标签
        label = QLabel("这是第一个标签页，拖拽窗口大小，内容会自动缩放：")
        tab_layout.addWidget(label)

        # 文本编辑框，默认就是Expanding策略，会自动占满剩余空间
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("在这里输入内容，窗口缩放时编辑区会跟着变大变小...")
        tab_layout.addWidget(text_edit)

        # 底部按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()  # 占位弹簧，把按钮推到右边
        save_btn = QPushButton("保存")
        save_btn.setFixedSize(80, 32)
        clear_btn = QPushButton("清空")
        clear_btn.setFixedSize(80, 32)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(clear_btn)
        tab_layout.addLayout(btn_layout)

        # 把页面添加到TabWidget
        self.tab_widget.addTab(tab1, "文本编辑")

    def add_form_tab(self):
        """第二个Tab：表单项页"""
        tab2 = QWidget()
        tab_layout = QVBoxLayout(tab2)
        tab_layout.setContentsMargins(15, 15, 15, 15)
        tab_layout.setSpacing(12)

        # 表单行1
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("用户名："))
        username_input = QLineEdit()
        username_input.setFixedHeight(30)
        row1.addWidget(username_input)
        tab_layout.addLayout(row1)

        # 表单行2
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("年龄："))
        age_spin = QSpinBox()
        age_spin.setFixedHeight(30)
        age_spin.setRange(1, 120)
        row2.addWidget(age_spin)
        row2.addStretch()  # 后面加弹簧，让输入框不会拉太宽
        tab_layout.addLayout(row2)

        # 加个大的文本框占满剩余空间
        tab_layout.addWidget(QLabel("备注信息："))
        remark_edit = QTextEdit()
        tab_layout.addWidget(remark_edit)

        self.tab_widget.addTab(tab2, "个人设置")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
