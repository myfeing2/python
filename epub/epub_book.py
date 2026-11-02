"""reading epub"""

import re
import os
import tempfile
import zipfile
import shutil
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

class EpubBook:
    def __init__(self):
        self.temp_dir = None
        self.book_path = ""
        self.book = None
        self.cover_doc = ""
        self.title = ""
        self.toc = []

    def extract_book(self, book_name:str):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.book_path = self.temp_dir.name
        zip_ref = zipfile.ZipFile(book_name, 'r')
        container = zip_ref.read('META-INF/container.xml').decode('utf-8')
        # 解析 XML 获取 full-path
        match = re.search(r'full-path="([^"]+)"', container)
        if match:
            opf_path = match.group(1)
        else:
            opf_path = ""
        #print(f"Extracting {book_name} to {self.book_path}")
        zip_ref.extractall(path=self.book_path)
        self.book = epub.read_epub(self.book_path)
        self.book_path = os.path.join(self.book_path, os.path.dirname(opf_path))
        self.title = self.book.get_metadata('DC', 'title')[0][0]
        self.toc = self.load_toc()
        self.find_cover_doc()

    def find_cover_doc(self):
        cover_meta = self.book.get_metadata('OPF', 'cover')
        if cover_meta:
            cover_id = cover_meta['content']
            self.cover_doc = self.book.get_item_with_id(cover_id).get_name()
            #print(f"cover_doc: {self.cover_doc}")
        else:
            #print("No cover metadata found.")
            item_id = self.book.spine[0][0]  # 获取第一个资源 ID
            self.cover_doc = self.book.get_item_with_id(item_id).get_name()
            '''
            for item_ref in self.book.spine:
                item_id = item_ref[0] # 获取资源 ID
                # 3. 根据 ID 获取具体的 EpubHtml 对象
                if "cover" == item_id.lower() or "titlepage" == item_id.lower():
                    self.cover_doc = self.book.get_item_with_id(item_id).get_name()
                    #print(f"Found cover document: {self.cover_doc}")
            '''

    def load_cover_doc(self) -> str:
        if self.cover_doc:
            return self.load_document(self.cover_doc)
        else:
            return ""
    
    def load_document(self, doc: str) -> str:
        item = self.book.get_item_with_href(doc)
        if item:
            return item.content.decode('utf-8')
        else:
            return ""

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
        contents = []
        for item in self.book.get_items():
            # 获取文档名称
            file_name = item.get_name()
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
                    file, ref = child['href'].split('#')
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
