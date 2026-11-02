"""
PySide6 QWebEngineView + QThread + QWebChannel 完整示例
功能：
1. Worker子线程后台生成数据，不卡UI
2. Python <-> JS 双向通信
3. 线程安全更新网页，避免崩溃
4. 窗口关闭时线程干净退出
"""
import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import QThread, Signal, QObject, QTimer, Slot, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel


# ====================== 1. 通信桥接对象（必须继承QObject）======================
class Bridge(QObject):
    """Python和JS通信的桥梁，所有跨语言调用都通过这个对象"""
    # 信号：Python -> JS 推送数据
    data_updated = Signal(str, float)  # 参数：消息文本、数值
    # 信号：线程状态更新
    status_changed = Signal(str)

    @Slot(str)  # 暴露给JS调用的方法，必须加@Slot装饰器
    def js_call_python(self, message):
        """JS调用Python的入口"""
        print(f"[JS 调用 Python] 收到消息: {message}")
        self.status_changed.emit(f"JS发来消息: {message}")
        return f"Python已收到: {message}"


# ====================== 2. Worker工作对象（子线程中运行）======================
class DataWorker(QObject):
    """后台数据生成/处理Worker，所有耗时操作放这里"""
    # 发出新数据的信号
    new_data = Signal(str, float)
    # 工作完成信号
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._is_running = False
        self.counter = 0

    @Slot()
    def start_work(self):
        """开始后台循环工作"""
        self._is_running = True
        print("[Worker线程] 开始工作")
        while self._is_running:
            time.sleep(1)  # 模拟耗时操作（比如读文件、网络请求、计算）
            self.counter += 1
            msg = f"第 {self.counter} 次更新"
            value = round(time.time() % 100, 2)
            # 发送新数据给主线程，绝对不要在这里直接操作webview！
            self.new_data.emit(msg, value)
            print(f"[Worker线程] 生成新数据: {msg}, {value}")
        self.finished.emit()

    @Slot()
    def stop_work(self):
        """停止工作"""
        self._is_running = False
        print("[Worker线程] 收到停止信号")


# ====================== 3. 主窗口（主线程，所有UI操作在这里）======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWebEngineView + 多线程示例")
        self.resize(1000, 700)

        # 初始化UI
        self._init_ui()
        # 初始化通信桥
        self.bridge = Bridge()
        # 初始化WebChannel
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)
        # 初始化线程和Worker
        self._init_thread()

        # 加载网页
        self._load_html()

        # 连接信号
        self._connect_signals()

    def _init_ui(self):
        """初始化界面控件"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 按钮栏
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("启动后台线程")
        self.btn_stop = QPushButton("停止后台线程")
        self.btn_js_call = QPushButton("Python调用JS")
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_js_call)
        layout.addLayout(btn_layout)

        # Web视图
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

    def _init_thread(self):
        """初始化Worker线程（推荐用moveToThread模式，而不是继承QThread）"""
        # 创建线程
        self.thread = QThread()
        # 创建Worker对象
        self.worker = DataWorker()
        # 将Worker移动到子线程
        self.worker.moveToThread(self.thread)

        # 线程启动时自动开始工作
        self.thread.started.connect(self.worker.start_work)
        # Worker完成时退出线程
        self.worker.finished.connect(self.thread.quit)
        # 线程退出时清理对象
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def _load_html(self):
        """加载内置HTML页面（也可以load本地文件/远程URL）"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Web页面</title>
    <style>
        body { font-family: "Microsoft Yahei", sans-serif; padding: 20px; background: #f5f5f5; }
        .card { background: white; border-radius: 8px; padding: 20px; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        #data-display { font-size: 24px; color: #2c3e50; font-weight: bold; }
        button { padding: 10px 20px; font-size: 16px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        #log { height: 200px; overflow-y: auto; background: #ecf0f1; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 13px; }
    </style>
</head>
<body>
    <h1>PySide6 QWebEngine 多线程演示</h1>
    
    <div class="card">
        <h3>后台线程实时数据：</h3>
        <div id="data-display">等待数据...</div>
    </div>

    <div class="card">
        <h3>JS调用Python：</h3>
        <button onclick="callPython()">点我调用Python方法</button>
    </div>

    <div class="card">
        <h3>通信日志：</h3>
        <div id="log"></div>
    </div>

    <!-- 引入QWebChannel的JS文件，PySide6自带，不用额外下载 -->
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
        let bridge = null;
        
        // 初始化QWebChannel连接
        new QWebChannel(qt.webChannelTransport, function(channel) {
            bridge = channel.objects.bridge;
            addLog("JS已连接到Python桥接对象");
            
            // 监听Python发来的数据更新信号
            bridge.data_updated.connect(function(msg, value) {
                addLog(`收到Python数据: ${msg}, 值=${value}`);
                document.getElementById("data-display").textContent = `${msg} | 当前值: ${value}`;
            });
            
            // 监听状态变化信号
            bridge.status_changed.connect(function(status) {
                addLog(`状态更新: ${status}`);
            });
        });

        function callPython() {
            if (!bridge) return;
            const result = bridge.js_call_python("你好Python，我是JS！");
            addLog(`调用Python返回结果: ${result}`);
        }

        function addLog(text) {
            const logEl = document.getElementById("log");
            const time = new Date().toLocaleTimeString();
            logEl.innerHTML += `[${time}] ${text}<br>`;
            logEl.scrollTop = logEl.scrollHeight;
        }

        // 暴露给Python调用的JS函数
        function calledByPython(param) {
            addLog(`Python调用了JS函数，参数: ${param}`);
            return "JS收到了！";
        }
    </script>
</body>
</html>
        """
        self.web_view.setHtml(html_content, QUrl("file:///"))

    def _connect_signals(self):
        """连接所有信号槽"""
        # 按钮事件
        self.btn_start.clicked.connect(self.start_background_thread)
        self.btn_stop.clicked.connect(self.stop_background_thread)
        self.btn_js_call.clicked.connect(self.call_js_from_python)

        # Worker新数据 -> 推送给JS（主线程操作webview，安全！）
        self.worker.new_data.connect(self.on_new_data_from_worker)

    def start_background_thread(self):
        """启动后台线程"""
        if not self.thread.isRunning():
            self.thread.start()
            self.bridge.status_changed.emit("后台线程已启动")

    def stop_background_thread(self):
        """停止后台线程"""
        if self.thread.isRunning():
            self.worker.stop_work()
            self.bridge.status_changed.emit("后台线程已停止")

    def on_new_data_from_worker(self, msg, value):
        """收到Worker线程的新数据，在主线程推送给JS（安全！）"""
        self.bridge.data_updated.emit(msg, value)

    def call_js_from_python(self):
        """Python主动调用JS函数"""
        js_code = 'calledByPython("来自Python的问候");'
        self.web_view.page().runJavaScript(js_code, lambda result: print(f"JS返回结果: {result}"))

    def closeEvent(self, event):
        """窗口关闭事件，保证线程干净退出，防止程序僵死"""
        if self.thread.isRunning():
            self.worker.stop_work()
            self.thread.quit()
            self.thread.wait(2000)  # 最多等2秒让线程退出
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
