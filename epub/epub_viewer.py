from fileinput import filename
import os
import sys
import json

from epub_book import EpubBook
from epub_reader import TtsTask

from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import (
    QObject,
    QThread,
    Slot,
)

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
    QToolBar,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QThread, Qt, QSize, QUrl

# 必须在创建 QApplication 之前设置
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
#os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
#os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9223"
os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_RHI_BACKEND"] = "opengl"
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
os.environ['MESA_LOADER_DRIVER_OVERRIDE'] = 'llvmpipe'
#os.environ['QT_QPA_PLATFORM'] = 'wayland'
os.environ['QT_OPENGL'] = 'software'
#os.environ["QT3D_RENDERER"] = "opengl"
#os.environ['QT_DEBUG_PLUGINS'] = "1"

basedir = os.path.dirname(__file__)
main_win = None

class Bridge(QObject):
    def __init__(self):
        super().__init__()
        self.label_id = set()
        self.label_id_above = ""
        self.last_vis_label_id = ""

    @Slot(str, result=str)
    def start_playback(self, first_sentence=None):
        main_win.start_playback(first_sentence)
        return f"start_playback of Python 收到: {first_sentence}"

    def clear_label_sets(self):
        self.label_id.clear()
        self.label_id_above = ""
        self.last_vis_label_id = ""

    @Slot(str, result=str)
    def add_visible(self, message):
        #print(f"add_visible of Python 收到: {message}")
        if self.label_id_above:
            main_win.deselect_above_visible(self.label_id_above)
            self.label_id_above = ""
        if self.last_vis_label_id:
            main_win.deselect_visible(self.last_vis_label_id)
            self.last_vis_label_id = ""
        self.label_id.add(message)
        main_win.select_visible(message)
        return f"add_visible of Python 收到: {message}"

    @Slot(str, result=str)
    def scroll_down(self, message):
        #print(f"scroll_down of Python 收到: {message}")
        if message in self.label_id:
            self.label_id.remove(message)
            if not self.label_id:
                self.last_vis_label_id = message
                main_win.select_visible(message)
            else:
                main_win.deselect_visible(message)
        return f"scroll_down of Python 收到: {message}"

    @Slot(str, result=str)
    def scroll_up(self, message):
        #print(f"scroll_up of Python 收到: {message}")
        if message in self.label_id:
            self.label_id.remove(message)
            if not self.label_id:
                self.label_id_above = message
                main_win.deselect_visible(message)
                main_win.select_above_visible(message)
            else:
                main_win.deselect_visible(message)
        return f"scroll_up of Python 收到: {message}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.epub = EpubBook()
        self.toc_tree = QTreeWidget()
        self.toc_tree.header().setVisible(False)
        self.toc_tree.itemClicked.connect(self.on_item_clicked)
        self.active_chapter = dict(name="", doc=self.epub.cover_doc, href='', view=None, reading_item=None)
        self.active_chapter['view'] = QWebEngineView()
        self.active_chapter['view'].loadFinished.connect(self.on_load_finished)

        self.playing = False
        self.first_entry = True
        self.ttstask = TtsTask()
        self.thread = QThread()
        self.ttstask.moveToThread(self.thread)
        self.ttstask.consumed.connect(self.send_next_text)
        self.ttstask.finished.connect(self.ttstask_stop)
        self.thread.started.connect(self.ttstask.run)  # 线程启动时执行任务

        self.setWindowTitle(self.epub.title)
        
        with open(os.path.join(basedir, "find_textnode.js"), "r", encoding="utf-8") as f:
            self.js_walkercode = f.read()

        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("bridge", self.bridge)
        self.active_chapter['view'].page().setWebChannel(self.channel)

        self.dev_view = QWebEngineView()
        self.dev_view.hide()  # 默认隐藏 DevTools
        self.doc_splitter = QSplitter(Qt.Vertical)
        self.doc_splitter.setStretchFactor(0, 3)  # 主视图宽一点
        self.doc_splitter.setStretchFactor(1, 2)  # DevTools 窄一点
        self.doc_splitter.addWidget(self.active_chapter['view'])
        self.doc_splitter.addWidget(self.dev_view)
        self.setCentralWidget(self.doc_splitter)
        self.active_chapter['view'].page().setDevToolsPage(self.dev_view.page())

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.toc_tree)
        self.main_splitter.addWidget(self.doc_splitter)
        self.main_splitter.setSizes([200, 400])
        self.main_splitter.setCollapsible(0, False)
        self.setCentralWidget(self.main_splitter)

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

        self.return_action = QAction(
            QIcon(os.path.join(basedir, "res/return.png")),
            "return",
            self,
        )
        self.return_action.triggered.connect(self.onReturnButtonClick)
        self.return_action.setEnabled(True)
        toolbar.addAction(self.return_action)

        self.cover_action = QAction(
            QIcon(os.path.join(basedir, "res/cover.png")),
            "cover",
            self,
        )
        self.cover_action.triggered.connect(self.onCoverButtonClick)
        self.cover_action.setEnabled(True)
        toolbar.addAction(self.cover_action)

        self.dev_view_action = QAction(
            QIcon(os.path.join(basedir, "res/dev_view.png")),
            "dev_view",
            self,
        )
        self.dev_view_action.triggered.connect(self.onDevViewButtonClick)
        self.dev_view_action.setEnabled(True)
        toolbar.addAction(self.dev_view_action)


    def closeEvent(self, event):
        #print("closing window...")
        if self.playing:
            self.playing = False
            self.first_entry = True
            self.ttstask.stop()
        event.accept()

    def on_load_finished(self, ok):
        if ok:
            #print("name: " + self.active_chapter['name'])
            #print("href: " + self.active_chapter['href'])
            self.bridge.clear_label_sets()
            if self.active_chapter['href']:
                self.scroll_to_text(self.active_chapter['href'])
            js = self.js_walkercode + f"\ninitWebChannel();\ninitEventListeners();"
            self.active_chapter['view'].page().runJavaScript(js)
            if self.playing:
                js_code = self.js_walkercode + "\nretrieveFirstSentence();"
                self.active_chapter['view'].page().runJavaScript(js_code, self.retrieve_sentence)
                self.first_entry = False
        else:
            print("loading page failure.")

    def scroll_to_text(self, target_id:str):
        # 转义目标文本，防止特殊字符破坏 JS 字符串
        escaped = target_id.replace("\\", "\\\\").replace("'", "\\'")
        js = self.js_walkercode + f"\nscrollToText('{escaped}');"
        self.active_chapter['view'].page().runJavaScript(js)

    def add_tree_items(self, toc:list, parent: QTreeWidgetItem):
        last_tree_item = parent
        for item in toc:
            if type(item) == tuple:
                tree_item = QTreeWidgetItem([item[2]])
                tree_item.setData(0, Qt.UserRole, {"doc":item[3], "href":item[4]})
                parent.addChild(tree_item)
                last_tree_item = tree_item
            else:
                self.add_tree_items(item, last_tree_item)

    def on_item_clicked(self, item, column):
        if self.epub.toc != []:
            self.active_chapter['name'] = item.text(0)
            doc, href = \
                item.data(0, Qt.UserRole).get("doc"), \
                item.data(0, Qt.UserRole).get("href")
            self.toc_tree.setCurrentItem(item)
            if self.active_chapter['doc'] == doc:
                self.scroll_to_text(href)
            else:
                self.active_chapter['doc'] = doc
                self.active_chapter['href'] = href
                #print(f"on_item_clicked: {self.active_chapter['doc']}, {self.active_chapter['href']}")
                html = self.epub.load_document(self.active_chapter['doc'])
                self.active_chapter['view'].setHtml(html, QUrl.fromLocalFile(os.path.join(self.epub.book_path, self.active_chapter['doc'])))
                if self.playing:
                    self.ttstask.stop()
                    self.first_entry = True
                    self.playing = False

    def select_visible(self, chapter_href):
        it = QTreeWidgetItemIterator(self.toc_tree)
        while it.value():
            item = it.value()
            # 处理 item
            item_doc = item.data(0, Qt.UserRole).get("doc")
            item_href = item.data(0, Qt.UserRole).get("href")
            if item_doc == self.active_chapter['doc'] and item_href == chapter_href:
                #print(f"  select_visible: {item.text(0)}")
                item.setSelected(True)
            it += 1

    def deselect_visible(self, chapter_href):
        it = QTreeWidgetItemIterator(self.toc_tree)
        while it.value():
            item = it.value()
            # 处理 item
            item_doc = item.data(0, Qt.UserRole).get("doc")
            item_href = item.data(0, Qt.UserRole).get("href")
            if item_doc == self.active_chapter['doc'] and item_href == chapter_href:
                #print(f"  deselect_visible: {item.text(0)}")
                item.setSelected(False)
            it += 1

    def select_above_visible(self, chapter_href):
        it = QTreeWidgetItemIterator(self.toc_tree)
        last_item = None
        while it.value():
            item = it.value()
            # 处理 item
            item_doc = item.data(0, Qt.UserRole).get("doc")
            item_href = item.data(0, Qt.UserRole).get("href")
            if item_doc == self.active_chapter['doc'] and item_href == chapter_href:
                #print(f"  select_above_visible: {item.text(0)}")
                if last_item:
                    last_item.setSelected(True)
            last_item = item
            it += 1

    def deselect_above_visible(self, chapter_href):
        it = QTreeWidgetItemIterator(self.toc_tree)
        last_item = None
        while it.value():
            item = it.value()
            # 处理 item
            item_doc = item.data(0, Qt.UserRole).get("doc")
            item_href = item.data(0, Qt.UserRole).get("href")
            if item_doc == self.active_chapter['doc'] and item_href == chapter_href:
                #print(f"  deselect_above_visible: {item.text(0)}")
                if last_item:
                    last_item.setSelected(False)
            last_item = item
            it += 1

    def get_reading_item(self, href):
        it = QTreeWidgetItemIterator(self.toc_tree)
        while it.value():
            item = it.value()
            item_href = item.data(0, Qt.UserRole).get("href")
            if item_href == href:
                return item
            it += 1
        return None

    @Slot()
    def send_next_text(self):
        js = self.js_walkercode + "\nretrieveNextSentence();"
        self.active_chapter['view'].page().runJavaScript(js, self.retrieve_sentence)

    def retrieve_sentence(self, value):
        value = json.loads(value)
        #print("retrieved sentence: ", value)
        #print(f'active_chapter: {self.active_chapter["reading_item"].text(0) if self.active_chapter["reading_item"] else "None"}, {self.active_chapter["href"]}')
        if value and value["sentence"]:
            self.ttstask.new_text_arrival(value["sentence"])
            if value["href"] != "" and value["href"] != self.active_chapter['href']:
                reading_item = self.get_reading_item(value["href"])
                #print(f"reading item {reading_item.text(0)}")
                if reading_item:
                    self.active_chapter['href'] = value["href"]
                    self.active_chapter["reading_item"] = reading_item
        else:
            #if no text, load next document, else stop
            next_item = self.toc_tree.itemBelow(self.active_chapter["reading_item"])
            #print(f"next_item: {next_item.text(0) if next_item else 'None'}")
            if next_item:
                self.toc_tree.setCurrentItem(next_item)
                self.active_chapter["reading_item"] = next_item
                self.active_chapter['doc'], \
                self.active_chapter['href'] = \
                    next_item.data(0, Qt.UserRole).get("doc"), \
                    next_item.data(0, Qt.UserRole).get("href")
                html = self.epub.load_document(self.active_chapter['doc'])
                self.active_chapter['view'].setHtml(html, QUrl.fromLocalFile(os.path.join(self.epub.book_path, self.active_chapter['doc'])))
            else:
                self.ttstask.stop()

    def start_playback(self, first_sentence=None):
        if not self.playing:
            self.playing = True
            self.thread.start()
            self.first_entry = False
        self.retrieve_sentence(first_sentence)

    @Slot()
    def ttstask_stop(self):
        self.playing = False
        self.first_entry = True
        self.thread.quit()
        self.thread.wait()

    def onOpenButtonClick(self, is_checked):
        self.onStopButtonClick(False)
        filters = "EPUB Files (*.epub);;All Files (*)"
        filename, selected_filter = QFileDialog.getOpenFileName(self, "Open File", "", filters)
        if filename:
            self.epub = EpubBook()
            self.epub.extract_book(filename)
            self.setWindowTitle(self.epub.title)
            self.toc_tree.clear()
            toc_root = self.toc_tree.invisibleRootItem()
            self.add_tree_items(self.epub.toc, toc_root)
            self.toc_tree.insertTopLevelItems(0, [toc_root])
            self.toc_tree.expandAll()
            self.active_chapter['doc'] = self.epub.cover_doc
            self.active_chapter['href'] = ''
            html = self.epub.load_cover_doc()
            path = os.path.join(self.epub.book_path, self.active_chapter['doc'])
            #print(f"onOpenButtonClick: {path}")
            self.active_chapter['view'].setHtml(html, QUrl.fromLocalFile(path))

    def onPlayButtonClick(self, is_checked):
        if not self.playing:
            self.playing = True
            self.thread.start()
            if self.first_entry:
                js_code = self.js_walkercode + "\nretrieveFirstSentence();"
            else:
                js_code = self.js_walkercode + "\nretrieveNextSentence();"
            self.active_chapter['view'].page().runJavaScript(js_code, self.retrieve_sentence)
            self.first_entry = False
        else:
            self.ttstask.play()

    def onPauseButtonClick(self, is_checked):
        if self.playing:
            self.ttstask.pause()

    def onStopButtonClick(self, is_checked):
        if self.playing:
            self.playing = False
            self.first_entry = True
            self.ttstask.stop()

    def onReturnButtonClick(self, is_checked):
        if self.playing:
            js_code = self.js_walkercode + "\nscrollToSentence();"
            self.active_chapter['view'].page().runJavaScript(js_code)
            selected = self.toc_tree.selectedItems()
            if selected:
                for item in selected:
                    item.setSelected(False)
            if self.active_chapter["reading_item"]:
                self.toc_tree.setCurrentItem(self.active_chapter["reading_item"])

    def onCoverButtonClick(self):
        if self.playing:
            self.ttstask.stop()
            self.first_entry = True
            self.playing = False
        self.active_chapter['doc'] = self.epub.cover_doc
        self.active_chapter['href'] = ''
        html = self.epub.load_cover_doc()
        path = os.path.join(self.epub.book_path, self.active_chapter['doc'])
        #print(f"onCoverButtonClick: {path}")
        self.active_chapter['view'].setHtml(html, QUrl.fromLocalFile(path))

    def onDevViewButtonClick(self):
        if self.dev_view.isVisible():
            self.dev_view.hide()
        else:
            self.dev_view.show()
            self.doc_splitter.setSizes([3, 2])  # 调整分割器大小，使 DevTools 可见

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
