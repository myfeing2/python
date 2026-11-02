### 3. 创建新的 EPUB 文件
from ebooklib import epub

def create_epub(output_path):
    # 初始化书籍对象
    book = epub.EpubBook()
        # 设置元数据
    book.set_identifier('id123456')
    book.set_title('Sample Book')
    book.set_language('zh')
    book.add_author('Author Name')
        # 添加 CSS 样式 (可选)
    style = '''body { font-family: sans-serif; }'''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
        # 创建章节
    chapter1 = epub.EpubHtml(title='Chapter 1', file_name='chap_1.xhtml', lang='zh')
    chapter1.content = '<h1>第一章</h1><p>这是第一章的内容。</p>'
    chapter1.add_item(nav_css) # 关联样式
    
    chapter2 = epub.EpubHtml(title='Chapter 2', file_name='chap_2.xhtml', lang='zh')
    chapter2.content = '<h1>第二章</h1><p>这是第二章的内容。</p>'
    chapter2.add_item(nav_css)
    
    # 添加章节到书籍
    book.add_item(chapter1)
    book.add_item(chapter2)
    
    # 定义目录和书脊 (阅读顺序)
    book.toc = [chapter1, chapter2]
    book.spine = ['nav', chapter1, chapter2]
    
    # 添加默认导航文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
        # 写入文件
    epub.write_epub(output_path, book, {})
    print(f"EPUB 已生成: {output_path}")

# 使用示例
# create_epub('new_book.epub')
