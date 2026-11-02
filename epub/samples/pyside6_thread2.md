PySide6 多线程的核心作用就是‌把耗时任务放到后台线程，避免界面卡死‌，同时通过‌信号与槽‌安全地把结果传回主线程更新 UI。目前主流的做法有两种：子类化 QThread 和 QRunnable + QThreadPool 线程池。

🧵 两种实现方式
‌子类化 QThread‌：继承 QThread，重写 run() 方法。适合需要较多控制的长期任务，但需要手动管理线程的生命周期，比如用 deleteLater() 释放资源。
‌QRunnable + QThreadPool‌：把任务封装成 QRunnable，提交给 QThreadPool 执行。线程的创建、回收、重用都交给线程池，省心很多，适合大量短期、独立的任务，比如批量处理文件或图片。‌‌
🔧 最推荐：moveToThread 模式
除了直接继承 QThread，还有一种更灵活的方式：把业务对象（QObject）通过 moveToThread() 移到一个普通的 QThread 里。这样可以把业务逻辑和线程生命周期解耦，也是很多开发者推荐的实践。‌‌

✅ 关键注意事项
‌不要用 Python 原生 threading 库‌：在 Qt 应用中，用 QThread 一体的集成性更好。
‌跨线程通信必须走信号与槽‌：子线程里‌绝对不能直接操作 UI 控件‌，否则会卡死甚至崩溃。正确做法是子线程只负责 emit 信号，主线程的槽函数去更新界面。
‌信号要定义在类上，不能定义在实例上‌：信号必须定义在 QObject 子类的类属性上，否则会报错。
‌QThread 对象要在主线程中创建‌：在子线程里创建 QThread 可能会导致两个事件循环并行，结果不可预知。
‌线程内的异常要自己捕获‌：子线程里的异常不会自动传到主线程，需要自己用 try-except 处理，或者通过信号把异常信息发出去。
‌优雅退出‌：不要用 terminate() 强制结束线程，推荐用 quit() 退出事件循环，配合 deleteLater() 让 Qt 自动回收内存。‌‌
🚀 快速上手代码
这是子类化 QThread 的最简模板，重点看‌信号与槽‌的用法：

python
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

class MyThread(QThread):
    # 1. 定义信号，用于把结果传回主线程
    result_ready = Signal(str)

    def run(self):
        # 2. 耗时任务在子线程执行
        time.sleep(3)  # 模拟耗时操作
        self.result_ready.emit("任务完成！")  # 3. 发信号

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("等待任务...")
        self.btn = QPushButton("开始任务")
        self.btn.clicked.connect(self.start_task)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def start_task(self):
        self.btn.setEnabled(False)
        self.thread = MyThread()  # 注意用 self 保存，防止被回收
        self.thread.result_ready.connect(self.on_result)  # 4. 连接信号到槽
        self.thread.start()

    def on_result(self, msg):
        self.label.setText(msg)
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
⚠️ 线程安全问题
如果多个线程要同时访问共享数据（比如全局变量），需要用 QMutex（互斥锁）或 QMutexLocker 保护临界区，防止数据竞争。‌‌
