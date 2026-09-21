import os
import sys

from ebooklib import epub
from epub_book import EpubBook
from epub_reader import TtsTask

from PySide6.QtCore import (
    QObject,
    QThread,
    QTimer,
    Signal,
    Slot,
)

from PySide6.QtGui import QColor, QPalette, QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    #QHBoxLayout,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QToolBar,
    QTabWidget,
    QWidget,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QThread, QUrl, Qt, QSize

# 必须在创建 QApplication 之前设置
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
#os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_RHI_BACKEND"] = "opengl"
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
os.environ['MESA_LOADER_DRIVER_OVERRIDE'] = 'llvmpipe'
os.environ['QT_QPA_PLATFORM'] = 'wayland'
#os.environ['QT_DEBUG_PLUGINS'] = "1"
#os.environ['QT_OPENGL'] = 'software'

basedir = os.path.dirname(__file__)
windows = []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.epub = EpubBook('epub/白板.epub')
        self.playing = False
        self.tts_counter = 1
        self.ttstask = TtsTask()
        self.thread = QThread()
        self.ttstask.moveToThread(self.thread)
        self.ttstask.consumed.connect(self.send_next_text)
        self.ttstask.finished.connect(self.ttstask_stop)
        self.thread.started.connect(self.ttstask.run)  # 线程启动时执行任务

        self.setWindowTitle(self.epub.title)

        self.toc_tree = QTreeWidget()
        self.toc_tree.itemClicked.connect(self.on_item_clicked)
        toc_root = self.toc_tree.invisibleRootItem()
        self.set_tree_items(self.epub.toc, toc_root)
        self.toc_tree.insertTopLevelItems(0, [toc_root])
        self.toc_tree.expandAll()

        self.active_chapter = dict(name="", doc=self.epub.first_doc, href='', view=None)
        self.active_chapter['view'] = QWebEngineView()
        self.active_chapter['view'].loadFinished.connect(self.on_load_finished)

        self.chapters = []
        self.chapters.append(self.active_chapter)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.toc_tree)
        splitter.addWidget(self.active_chapter['view'])
        splitter.setSizes([250, 600])
        splitter.setCollapsible(0, False)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMinimumSize(QSize(800, 600))
        self.tabs.addTab(splitter, self.active_chapter['name'])
        self.setCentralWidget(self.tabs)

        self.dev_view = QWebEngineView()
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setStretchFactor(0, 3)  # 主视图宽一点
        main_splitter.setStretchFactor(1, 2)  # DevTools 窄一点
        main_splitter.addWidget(self.tabs)
        main_splitter.addWidget(self.dev_view)
        self.setCentralWidget(main_splitter)
        self.active_chapter['view'].page().setDevToolsPage(self.dev_view.page())

        toolbar = QToolBar("main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.openbook_action = QAction(
            QIcon(os.path.join(basedir, "res/book-open.png")),
            "open",
            self,
        )
        self.openbook_action.triggered.connect(self.onOpenButtonClick)
        self.openbook_action.setEnabled(True)
        toolbar.addAction(self.openbook_action)

        self.tabplus_action = QAction(
            QIcon(os.path.join(basedir, "res/tab-plus.png")),
            "play",
            self,
        )
        self.tabplus_action.triggered.connect(self.onTabplusButtonClick)
        self.tabplus_action.setEnabled(True)
        toolbar.addAction(self.tabplus_action)

        self.play_action = QAction(
            QIcon(os.path.join(basedir, "res/play.png")),
            "open",
            self,
        )
        self.play_action.triggered.connect(self.onPlayButtonClick)
        self.play_action.setEnabled(True)
        self.play_action.setToolTip('开始朗读')
        toolbar.addAction(self.play_action)

        self.pause_action = QAction(
            QIcon(os.path.join(basedir, "res/pause.png")),
            "pause",
            self,
        )
        self.pause_action.triggered.connect(self.onPauseButtonClick)
        self.pause_action.setEnabled(True)
        toolbar.addAction(self.pause_action)

        self.stop_action = QAction(
            QIcon(os.path.join(basedir, "res/stop.png")),
            "stop",
            self,
        )
        self.stop_action.triggered.connect(self.onStopButtonClick)
        self.stop_action.setEnabled(True)
        toolbar.addAction(self.stop_action)

    def on_load_finished(self, ok):
        if ok:
            print("href: " + self.active_chapter['href'])
            if self.active_chapter['href']:
                self.scroll_to_text(self.active_chapter['href'])
                self.active_chapter['view'].page().runJavaScript("window.currEle=null;window.currRange=null;")
                #self.active_chapter['view'].page().runJavaScript("console.log(window.myGlobalVar);")
        else:
            print("loading page failure.")

    def scroll_to_text(self, target_id:str):
        # 转义目标文本，防止特殊字符破坏 JS 字符串
        escaped = target_id.replace("\\", "\\\\").replace("'", "\\'")
        js = f"""
        (function() {{
            // 在页面所有元素中查找包含目标文本的元素
            const walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_ELEMENT, {{
                    acceptNode(node) {{
                        return node.id === '{escaped}'
                            ? NodeFilter.FILTER_ACCEPT
                            : NodeFilter.FILTER_SKIP;
                    }}
                }}
            );
            const node = walker.nextNode();
            console.log(node)
            if (node) {{
                //node.parentElement.scrollIntoView({{behavior: 'auto', block: 'start'}});
                node.scrollIntoView({{behavior: 'auto', block: 'start'}});
            }}
        }})();
        """
        self.active_chapter['view'].page().runJavaScript(js)

    def on_item_clicked(self, item, column):
        if self.epub.toc != []:
            self.active_chapter['name'], self.active_chapter['doc'], self.active_chapter['href'] = self.epub.search_chapter(item.data(0, Qt.UserRole), self.epub.toc)
            html = self.epub.load_document(self.active_chapter['doc'])
            self.active_chapter['view'].setHtml(html)
            self.tabs.setTabText(self.tabs.currentIndex(), self.active_chapter['name'])

    def set_tree_items(self, toc:list, parent: QTreeWidgetItem):
        last_tree_item = parent
        for item in toc:
            if type(item) == tuple:
                tree_item = QTreeWidgetItem([item[2]])
                tree_item.setData(0, Qt.UserRole, item[1])
                parent.addChild(tree_item)
                last_tree_item =  tree_item
            else:
                self.set_tree_items(item, last_tree_item)

    def send_next_text(self):
        if self.tts_counter < 2:
            self.tts_counter += 1
            #self.ttstask.new_text_arrival("希望能够在未来的artificial intelligence领域有所建树。")
        else:
            self.ttstask.stop()

    def find_textnode_in_viewport(self):
        js = """
            const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
            const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
            elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, dt, dd, blockquote, td, th, span, div')
            for (const el of elements) {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);

                // 过滤不可见元素：尺寸为0、display:none、visibility:hidden
                if (!Array.from(el.childNodes).some(node => node.nodeType === 3)) continue;

                const text = Array.from(el.childNodes).filter(node => node.nodeType === 3);
                if (!text) continue;
                if (el.offsetParent === null) continue; 
                if (rect.width === 0 || rect.height === 0) continue;
                if (style.display === 'none' || style.visibility === 'hidden') continue;

                // 判断是否在视口内（任意部分可见就算）
                const isInViewport = (
                    rect.top < viewportHeight && rect.bottom > 0 &&
                    rect.left < viewportWidth && rect.right > 0
                );

                if (isInViewport) {
                    //console.log(el.textContent);
                    window.currEle = el;
                    return true;
                } else
                    window.currEle = null
                    return false;
            }
        """
        self.active_chapter['view'].page().runJavaScript(js, self.after_find_textnode)

    def after_find_textnode(self, ok):
        if ok:
            pass
        else:
            pass

    def ttstask_stop(self):
        self.playing = False
        self.tts_counter = 1
        self.thread.quit()
        self.thread.wait()

    def onOpenButtonClick(self, is_checked):
        pass

    def onTabplusButtonClick(self, is_checked):
        pass
    
    def onPlayButtonClick(self, is_checked):
        if not self.playing:
            self.playing = True
            #self.ttstask.new_text_arrival("让机器能够用自然流畅的语音与人类进行交流")
            self.thread.start()
        else:
            self.ttstask.play()

    def onPauseButtonClick(self, is_checked):
        if self.playing:
            self.ttstask.pause()

    def onStopButtonClick(self, is_checked):
        if self.playing:
            self.ttstask.stop()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    windows.append(main_win)
    main_win.show()
    sys.exit(app.exec())
