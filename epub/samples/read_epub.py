import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def read_epub_info(epub_path):
    # 读取 EPUB 文件
    book = epub.read_epub(epub_path)

    # 获取元数据 (返回值为列表，通常取第一个元素)
    title = book.get_metadata('DC', 'title')
    author = book.get_metadata('DC', 'creator')
    language = book.get_metadata('DC', 'language')

    print(f"标题: {title if title else 'N/A'}")
    print(f"作者: {author if author else 'N/A'}")
    print(f"语言: {language if language else 'N/A'}")

    # 遍历所有文档项 (XHTML/HTML)
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        print(f"文件名: {item.get_name()}")

        # 解析 HTML 内容
        soup = BeautifulSoup(item.get_content(), 'lxml')

        # 提取纯文本 (去除标签)
        text = soup.get_text(separator='\n', strip=True)
        if text:
            print(f"内容预览: {text[:100]}...")

# 使用示例
read_epub_info('白板.epub')
