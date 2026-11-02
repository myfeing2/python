PySide6 里用 QWebEngineView 做嵌入浏览器，再结合多线程，核心就一句话：‌耗时任务放子线程，UI 操作（包括 QWebEngineView 的加载、刷新、执行 JS）永远留在主线程‌。所有界面更新，只能通过信号槽把数据传回主线程来做。‌‌

⚙️ 常见场景：子线程生成数据，主线程刷新网页
这是最典型的用法，比如子线程读文件、抓数据，然后让网页定时刷新。可以参考这个思路：‌‌

‌子线程‌（QThread 子类）：负责耗时操作，处理完发一个信号（比如带文件路径的 str）。
‌主线程‌：接收信号后，调用 QWebEngineView 的 load() 或 setHtml() 来更新页面。
python
# 子线程
class RefreshThread(QThread):
    url_ready = Signal(str)

    def run(self):
        while True:
            #... 生成新的 html 路径或数据
            self.url_ready.emit(path)
            time.sleep(10)

# 主线程
self.thread = RefreshThread()
self.thread.url_ready.connect(self.update_web)
self.thread.start()

def update_web(self, path):
    self.web_view.load(QUrl.fromLocalFile(path))
直接继承 QThread 能跑，但更推荐官方推荐的 ‌Worker + moveToThread()‌ 模式，代码更清晰，也避免生命周期管理的坑。‌‌

⚠️ 必须避开的坑
‌子线程直接操作 QWebEngineView 会崩‌：Qt 的 UI 对象不是线程安全的，子线程里调用 load()、setHtml() 这类方法会导致程序崩溃（Cannot send events to objects owned by a different thread）。
‌线程退出要干净‌：窗口关闭时，如果子线程还在跑，程序会退不出去。记得在 closeEvent 里调用 thread.quit() 和 thread.wait()。
‌QWebEngine 本身是多进程的‌：它基于 Chromium，底层有自己的多进程架构（渲染、网络、GPU 都是独立进程），这跟你的 Python 多线程是两码事，别混在一起理解。
‌频繁刷新有技巧‌：不要用 stop() + reload() 来更新页面，不一定生效。正确做法是把新 HTML 内容通过信号传给主线程，再调用 setHtml() 更新。‌‌
🔗 与前端 JS 的通信（QWebChannel）
如果要在网页 JS 和 Python 之间双向传数据，配合多线程也是这个原则：‌‌

‌Python 端‌：创建一个继承 QObject 的桥接类，用 @Slot 装饰暴露给 JS 的方法，用 Signal 定义主动推送给 JS 的事件。
‌初始化‌：创建 QWebChannel，用 registerObject() 注册桥接对象，再绑定到页面上。
‌JS 端‌：加载 qwebchannel.js，连接上之后就能直接调用 Python 方法、监听 Python 信号。
‌传递复杂数据时要注意‌：信号槽跨线程传自定义类型（比如 DataFrame）必须先注册类型，否则信号会丢失，界面不更新。‌‌

另外，如果后台任务只是偶尔发个数据给网页，也可以用 QTimer 单次触发来替代多线程，逻辑更简单。‌‌

=================================

先安装依赖，然后直接运行脚本即可：

bash
pip install pyside6
python pyside6_web_thread_demo.py

📋 代码结构说明
我用了官方推荐的 ‌Worker + moveToThread‌ 模式（比直接继承QThread更灵活、更不容易踩坑），整体分三层：

表格
模块	所在线程	职责
Bridge 桥接对象	主线程	Python和JS之间的通信中转，通过信号槽传递数据
DataWorker 工作对象	子线程	所有耗时操作（读文件、网络请求、计算）都放这里，绝对不碰UI
MainWindow 主窗口	主线程	所有UI操作（包括QWebEngineView的加载、执行JS）都在这里
✅ 已经帮你避开的所有坑
线程安全‌：子线程只发信号，绝不直接操作QWebEngineView，不会触发Cannot send events to objects owned by a different thread崩溃
干净退出‌：重写了closeEvent，窗口关闭时会先停止Worker、等待线程退出，不会出现关了窗口程序还在后台跑的情况
QWebChannel内置‌：JS里引入的qrc:///qtwebchannel/qwebchannel.js是PySide6自带的，不需要你额外下载文件
双向通信‌：既支持Python后台线程推数据给JS实时刷新，也支持JS按钮点击调用Python方法
runJavaScript回调‌：Python调用JS函数时可以拿到返回值，方便你做后续处理
💡 你可以直接修改扩展的地方
如果要加载本地HTML文件，把self.web_view.setHtml(...)改成self.web_view.load(QUrl.fromLocalFile("你的文件路径.html"))即可
如果要加载远程网页，直接用self.web_view.load(QUrl("https://xxx.com"))
把DataWorker.start_work()里的time.sleep(1)替换成你自己的耗时逻辑（读串口、爬数据、处理大文件等）即可
需要传递复杂数据（字典、列表）的话，信号参数用str类型，json序列化后传过去，JS里JSON.parse就行
运行起来你会看到：点击「启动后台线程」后，网页会每秒自动更新一次数据；点击JS按钮可以调用Python，点击「Python调用JS」按钮可以主动调用网页里的函数，全程UI完全不卡顿。
