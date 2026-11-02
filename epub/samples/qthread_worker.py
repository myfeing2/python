import sys
import time
from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel

class Worker(QObject):
    progress = Signal(int)      # 向主线程发进度
    finished = Signal()         # 任务完成

    @Slot()
    def run_task(self):
        for i in range(100):
            time.sleep(0.05)
            self.progress.emit(i)
        self.finished.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("等待任务...")
        self.btn = QPushButton("开始")
        self.btn.clicked.connect(self.start_task)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)          # 关键：把 worker 移到子线程
        self.thread.started.connect(self.worker.run_task)  # 线程启动时执行任务
        self.worker.progress.connect(self.on_progress)     # 子线程信号 → 主线程槽
        self.worker.finished.connect(self.on_finished)

    def start_task(self):
        self.btn.setEnabled(False)
        self.thread.start()

    def on_progress(self, value):
        self.label.setText(f"进度: {value}")

    def on_finished(self):
        self.thread.quit()
        self.thread.wait()
        self.btn.setEnabled(True)
        self.label.setText("完成！")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())

'''
⚠️ 三个关键前提
‌Worker 必须继承 QObject‌，且‌不能有父对象‌，否则 moveToThread 不生效（不报错但白搭）。
‌信号必须定义在类上，不能定义在实例上‌，否则会报 'Signal' object has no attribute 'connect'。
‌子线程里绝对不能直接操作 UI‌（改文本、更新按钮都不行），必须通过信号发回主线程再更新。‌‌
❌ 常见坑
‌不要手动调用 QThread.run()‌，用 start() 启动，配合 started 信号触发 Worker 的槽函数。
‌不要用 terminate() 强制杀线程‌，容易资源泄露。正确做法是设置停止标志位（比如 self.running = False），让任务自己退出循环，再 quit() + wait()。
‌跨线程传自定义类型‌（如 numpy.array、未注册的 Python 类）需要先用 qRegisterMetaType() 注册，否则可能崩溃。
‌lambda 间接调用 Worker 槽函数会失效‌——槽函数必须在子线程里被直接调用，some_signal.connect(lambda: worker.func()) 这种写法不会让 func() 跑在子线程。‌‌
'''
