import os
import zipfile
from ebooklib import epub

def get_oebps_path(epub_path):
    with zipfile.ZipFile(epub_path) as z:
        container = z.read('META-INF/container.xml').decode('utf-8')
        # 解析 XML 获取 full-path
        import re
        match = re.search(r'full-path="([^"]+)"', container)
        if match:
            opf_path = match.group(1)
            return os.path.dirname(opf_path)
    return None

# 使用 ebooklib 读取后，item 路径相对 OEBPS
book = epub.read_epub('book.epub')
oebps = get_oebps_path('book.epub')
for item in book.get_items():
    full_path = f"{oebps}/{item.file_name}"
    print(full_path)
