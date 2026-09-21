"""reading epub"""

import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

class EpubBook:
    def __init__(self, book_path:str):
        self.book_path = book_path
        self.book = epub.read_epub(book_path)
        self.first_doc = ""
        self.title = self.book.get_metadata('DC', 'title')[0][0]
        self.toc = self.load_toc()

    def load_first_doc() -> str:
        return load_document(self.first_doc)
    
    def load_document(self, doc: str) -> str:
        item = self.book.get_item_with_href(doc)
        html = ""
        if item:
            html = item.get_content().decode('utf-8')
        return html

    def get_text(self, html:str) -> str:
        soup = BeautifulSoup(html, 'lxml')
        text = ""
        for child in soup.descendants:
            text = text + child.get_text()
        return text

    def split_text(self, text:str) -> list:
        return re.split(r'[,.;?!，。；？！]', text)

    def load_toc(self):
        # 遍历所有文档项 (XHTML/HTML)
        for item in self.book.get_items():
            file_name = item.get_name()
            if item.get_type() == ebooklib.ITEM_COVER:
               self.first_doc = file_name
            if file_name.endswith('.ncx'):
                soup = BeautifulSoup(item.get_content(), 'xml')
                root = soup.find("navMap")
                id = {'id':0}
                contents = self.build_toc_ver2(root, -1, id)
                break
            elif file_name.endswith("nav.xhtml"):
                soup = BeautifulSoup(item.get_content(), 'xml')
                root = soup.find("nav")
                id = {'id':0}
                contents = self.build_toc_ver3(root, 0, id)
                break
        return contents

    def build_toc_ver3(self, root:BeautifulSoup, tier:int, id:dict) -> list:
        value = []
        for child in root.children:
            if child.name == "ol":
                tier += 1
                value.append(self.build_toc_ver3(child, tier, id))
            elif child.name == 'li':
                value.append(self.build_toc_ver3(child, tier, id))
            elif child.name == 'span':
                id['id'] += 1
                value.append((tier, id['id'], child.get_text(), None, None))
            elif child.name == 'a':
                id['id'] += 1
                if child['href'].find('#') != -1:
                    file, ref = href.split('#')
                else:
                    file = child['href']
                    ref = None
                value.append((tier, id['id'], child.get_text(), file, ref))
        return value

    def build_toc_ver2(self, root:BeautifulSoup, tier:int, id:dict) -> list:
        value = []
        tier += 1
        for child in root.children:
            if child.name == "navLabel":
                label = child.find('text').get_text()
            elif child.name == 'content':
                if child['src'].find('#') != -1:
                    file, ref = child['src'].split('#')
                else:
                    file = child['src']
                    ref = None
                value.append((tier, id['id'], label, file, ref))
            elif child.name == "navPoint":
                id['id'] += 1
                value.append(self.build_toc_ver2(child, tier, id))
        return value

    def search_chapter(self, id:int, toc:list) -> tuple:
        res = ()
        for c in toc:
            if type(c) == tuple:
                if c[1] == id:
                    res = (c[2], c[3], c[4])
                    break
            else:
                res = self.search_chapter(id, c)
                if res != ():
                    break
        return res

    def print_toc(self, toc:list):
        for c in toc:
            if type(c) == tuple:
                print(''.zfill(c[0]-1).replace('0', ' ', c[0]-1) + str(c))
            else:
                if c == []:
                    print('empty list.')
                else:
                    self.print_toc(c)
