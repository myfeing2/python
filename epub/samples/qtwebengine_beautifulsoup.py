'''
PySide6 + QtWebEngine + BeautifulSoup 这个组合，核心思路是：‌用 QtWebEngine 渲染页面，用 BeautifulSoup 解析页面结构，两者通过“抓取 HTML 字符串”这一步同步起来‌。也就是说，不是让 BeautifulSoup 直接解析网络请求，而是先让 WebEngine 把渲染完的完整 HTML 拿回来，再交给 BeautifulSoup 处理。

🧩 工作流程
‌创建 QWebEngineView 并加载页面‌：用 QWebEngineView 加载目标 URL，等待页面渲染完成（包括 JS 动态生成的内容）。
‌提取渲染后的 HTML‌：通过 page().toHtml(callback) 异步拿到完整 HTML 字符串。这是关键——只有这里拿到的才是渲染后的最终 DOM，直接 requests.get() 拿不到 JS 生成的内容。
‌用 BeautifulSoup 解析‌：把拿到的 HTML 字符串传入 BeautifulSoup(html, 'lxml')，然后正常提取数据。
💻 核心代码示例
python
'''

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from bs4 import BeautifulSoup

app = QApplication(sys.argv)
view = QWebEngineView()
view.load(QUrl("https://example.com"))

def on_load_finished(ok):
    if ok:
        # 关键：异步获取渲染后的 HTML
        view.page().toHtml(lambda html: parse_html(html))
    else:
        print("页面加载失败")

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    # 正常使用 BeautifulSoup 提取数据
    titles = [h.text.strip() for h in soup.find_all('h1')]
    print(titles)
    app.quit()

view.loadFinished.connect(on_load_finished)
view.show()
sys.exit(app.exec())

'''
⚠️ 几个要注意的坑
‌同步 vs 异步‌：toHtml() 是异步回调，不是同步返回。如果想让整个流程看起来“同步”，可以用 QEventLoop 配合信号转成同步等待，但小心页面加载失败导致事件循环卡死。
‌安装包‌：PySide6 通常自带 QtWebEngine，但有时需要单独装 pip install PySide6-QtWebEngine；另外建议装 lxml 作为解析器，比默认的 html.parser 快不少。
‌数据提取场景‌：如果页面内容是纯静态的（没有 JS 渲染），直接用 requests + BeautifulSoup 就够，完全不用 QtWebEngine，省资源且更简单；只有页面需要执行 JS 才上 QtWebEngine。‌
📌 实际应用建议
这种组合适合做‌需要登录态、或依赖 JS 渲染的页面数据抓取‌，比如股票行情、动态加载的列表页等。QtWebEngine 负责模拟浏览器环境拿到真实渲染结果，BeautifulSoup 负责快速结构化提取，比用 Selenium 轻量，又比纯 requests 能处理更多场景。
'''
