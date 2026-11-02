import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PySide6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 定义高亮规则：(正则表达式, 格式对象)
        self.highlighting_rules = []

        # 1. 关键字高亮 (蓝色加粗)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#2E8B57"))  # SeaGreen
        keyword_format.setFontWeight(QFont.Bold)
        
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda",
            "None", "nonlocal", "not", "or", "pass", "raise", "return",
            "True", "try", "while", "with", "yield"
        ]
        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # 2. 字符串高亮 (灰色)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#A9A9A9"))  # DarkGray
        # 匹配双引号或单引号字符串
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # 3. 注释高亮 (绿色斜体)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#008000"))  # Green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#[^\n]*"), comment_format))

    def highlightBlock(self, text):
        """
        对每一行文本执行高亮逻辑
        """
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 文本高亮示例")
        self.resize(600, 400)

        # 使用 QTextEdit 或 QPlainTextEdit
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # 初始化高亮器，传入文档对象
        self.highlighter = PythonHighlighter(self.editor.document())
        
        # 设置示例文本
        sample_code = """
def hello_world():
    # 这是一个注释
    name = "PySide6"
    if name == "PySide6":
        print("Hello, " + name)
    return True
"""
        self.editor.setText(sample_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

'''
关键点说明：
‌继承 QSyntaxHighlighter‌：必须子类化此类，构造函数中需调用 super().__init__(parent)，其中 parent 通常是 QTextDocument 对象（通过 edit.document() 获取）。
‌重写 highlightBlock(self, text)‌：Qt 会自动遍历文档的每一行并调用此方法。text 参数是当前行的字符串内容。
‌使用 QRegularExpression‌：相比旧的 QRegExp，QRegularExpression 性能更好且支持更标准的正则语法。使用 globalMatch 获取所有匹配项。
‌应用格式 setFormat(start, length, format)‌：在匹配到的位置应用 QTextCharFormat，可设置前景色、背景色、字体粗细等。
‌自动更新‌：当用户编辑文本时，QSyntaxHighlighter 会自动重新计算受影响行的高亮，无需手动触发。
'''
