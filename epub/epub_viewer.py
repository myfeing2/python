import os
import sys
import json

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
os.environ['QT_OPENGL'] = 'software'
#os.environ["QT3D_RENDERER"] = "opengl"
#os.environ['QT_DEBUG_PLUGINS'] = "1"

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
        
        with open(os.path.join(basedir, "find_textnode.js"), "r", encoding="utf-8") as f:
            self.js_walkercode = f.read()
        
        self.toc_tree = QTreeWidget()
        self.toc_tree.itemClicked.connect(self.on_item_clicked)
        toc_root = self.toc_tree.invisibleRootItem()
        self.add_tree_items(self.epub.toc, toc_root)
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
        splitter.setSizes([200, 400])
        splitter.setCollapsible(0, False)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMinimumSize(QSize(600, 200))
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
            "play",
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
            if (node) {{
                node.scrollIntoView({{behavior: 'auto', block: 'start'}});
            }}
        }})();
        """
        self.active_chapter['view'].page().runJavaScript(js)

    def on_item_clicked(self, item, column):
        if self.epub.toc != []:
            self.active_chapter['name'], \
            self.active_chapter['doc'], \
            self.active_chapter['href'] = \
                self.epub.search_chapter(item.data(0, Qt.UserRole), self.epub.toc)
            html = self.epub.load_document(self.active_chapter['doc'])
            self.active_chapter['view'].setHtml(html)
            self.tabs.setTabText(self.tabs.currentIndex(), self.active_chapter['name'])

    def add_tree_items(self, toc:list, parent: QTreeWidgetItem):
        last_tree_item = parent
        for item in toc:
            if type(item) == tuple:
                tree_item = QTreeWidgetItem([item[2]])
                tree_item.setData(0, Qt.UserRole, item[1])
                parent.addChild(tree_item)
                last_tree_item = tree_item
            else:
                self.add_tree_items(item, last_tree_item)

    def moveto_next_treeitem(self, chapter_href):
        curr_item = self.toc_tree.currentItem()
        if curr_item:
            next_item = self.toc_tree.itemBelow(curr_item)
            if next_item:
                name, doc, href = self.epub.search_chapter(next_item.data(0, Qt.UserRole), self.epub.toc)
                if doc == self.active_chapter['doc'] and href == chapter_href:
                    self.toc_tree.setCurrentItem(next_item)
                    self.tabs.setTabText(self.tabs.currentIndex(), name)
                    self.active_chapter['name'] = name
                    self.active_chapter['href'] = href

    def send_next_text(self):
        js = self.js_walkercode + "\nretrieveNextSentence();"
        self.active_chapter['view'].page().runJavaScript(js, self.retrieve_sentence)

    def retrieve_sentence(self, value):
        value = json.loads(value)
        if value["sentence"] != "":
            print("sentence: " + value["sentence"])
            self.ttstask.new_text_arrival(value["sentence"])
            self.moveto_next_treeitem(value["href"])
        else:
            #if no text, load next document, else stop
            self.ttstask.stop()

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
            self.tabs.currentWidget().setDisabled(True)
            self.thread.start()
            js_code = self.js_walkercode + "\nretrieveFirstSentence();"
            self.active_chapter['view'].page().runJavaScript(js_code, self.retrieve_sentence)
        else:
            self.ttstask.play()

    def onPauseButtonClick(self, is_checked):
        if self.playing:
            self.ttstask.pause()

    def onStopButtonClick(self, is_checked):
        if self.playing:
            self.playing = False
            self.ttstask.stop()
            self.tabs.currentWidget().setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    windows.append(main_win)
    main_win.show()
    sys.exit(app.exec())
