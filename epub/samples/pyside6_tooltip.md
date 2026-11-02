PySide6 里给控件加 tooltip 很简单，核心就是 setToolTip() 方法，鼠标悬停时就会显示提示文字。‌

python
button = QPushButton("Hover Over Me")
button.setToolTip("Click this button to continue.")
📌 基本用法
‌设置提示‌：任何继承自 QWidget 的控件都能调用 setToolTip("文本")，比如按钮、输入框、标签、窗口本身都行。
‌获取提示‌：用 toolTip() 方法可以拿到当前设置的提示文本。
‌多控件独立设置‌：每个控件可以分别设置自己的 tooltip，互不影响，适合给界面上每个元素做简短说明。‌
🎨 富文本与样式
‌支持简单 HTML‌：setToolTip() 里可以直接用 HTML 标签，比如 <b> 加粗、<br> 换行，让提示更清晰。
python
button.setToolTip("<b>Save File</b><br>Click to save the current document.")
‌延迟显示‌：用 setToolTipDuration(毫秒) 可以控制悬停多久才显示提示。
‌全局样式‌：用样式表统一美化所有 tooltip，比如改背景色、边框：
python
app.setStyleSheet("""
    QToolTip {
        background-color: #ffffe0;
        color: black;
        border: 1px solid black;
    }
""")
```‌

⚠️ 注意：setToolTip() 只负责悬停提示，和状态栏提示 setStatusTip() 是两回事，别搞混。‌