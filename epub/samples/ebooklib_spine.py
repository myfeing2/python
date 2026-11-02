from ebooklib import epub
from bs4 import BeautifulSoup # 用于提取纯文本，需 pip install beautifulsoup4

def get_chapters_in_order(epub_path):
    # 1. 读取 EPUB 文件
    book = epub.read_epub(epub_path)
    
    chapters = []
    
    # 2. 遍历 spine 获取阅读顺序
    # spine 结构示例: [('chap_01', 'yes'), ('chap_02', 'yes'), ...]
    for item_ref in book.spine:
        item_id = item_ref[0] # 获取资源 ID
        
        # 3. 根据 ID 获取具体的 EpubHtml 对象
        item = book.get_item_with_id(item_id)
        
        # 确保它是文档类型（排除可能混入的非线性资源或错误引用）
        if item and item.get_type() == epub.ITEM_DOCUMENT:
            chapters.append(item)
            
    return chapters

# 使用示例
if __name__ == '__main__':
    book_path = 'your_book.epub'
    ordered_chapters = get_chapters_in_order(book_path)
    
    for i, chapter in enumerate(ordered_chapters):
        print(f"--- 第 {i+1} 章: {chapter.title} ---")
        # 获取 HTML 内容
        html_content = chapter.get_body_content_str()
        # 使用 BeautifulSoup 提取纯文本（可选）
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        print(text[:200]) # 打印前200个字符
        print("...\n")
