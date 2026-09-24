'''
根因：工作线程（QThread 或 Worker 对象）在信号发出前已被 Python 垃圾回收或显式销毁，导致 Qt 尝试访问已释放的 C++ 对象内存。常见于未保持线程/对象引用、窗口关闭时未正确断开连接或停止线程。

修复方案：

保持 QThread/Worker 实例为类成员变量，防止被 GC 回收。
使用 deleteLater() 安全销毁对象。
在窗口关闭或任务结束前，先断开信号连接并等待线程退出。
python
'''

import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal, Slot

class Worker(QThread):
    progress = Signal(int)
    
    def run(self):
        for i in range(10):
            if self.isInterruptionRequested():
                break
            time.sleep(0.5)
            self.progress.emit(i * 10)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread Fix Demo")
        
        # 关键：将线程对象作为实例属性保存，防止被垃圾回收
        self.worker = None
        layout = QVBoxLayout()
        self.label = QLabel("Ready")
        self.btn_start = QPushButton("Start Task")
        self.btn_stop = QPushButton("Stop Task")
        
        layout.addWidget(self.label)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.btn_start.clicked.connect(self.start_task)
        self.btn_stop.clicked.connect(self.stop_task)

    def start_task(self):
        if self.worker and self.worker.isRunning():
            return
            
        # 创建新线程实例
        self.worker = Worker()
        # 连接信号，注意使用 lambda 或 partial 避免循环引用问题，或直接连接槽
        self.worker.progress.connect(self.update_ui)
        # 线程结束后自动清理资源
        self.worker.finished.connect(self.on_worker_finished)
                self.worker.start()
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    @Slot(int)
    def update_ui(self, value):
        self.label.setText(f"Progress: {value}%")

    def stop_task(self):
        if self.worker:
            self.worker.requestInterruption()
            # 不要直接 delete，等待 finished 信号

    def on_worker_finished(self):
        # 线程自然结束或被中断后执行
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        # 可选：显式删除 worker 对象，但通常由 Python GC 处理即可
        # self.worker.deleteLater()         self.worker = None

    def closeEvent(self, event):
        # 窗口关闭时确保线程安全退出
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait(2000)  # 最多等待2秒
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
