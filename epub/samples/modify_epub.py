import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def modify_epub(input_path, output_path):
    book = epub.read_epub(input_path)
    
    # 遍历所有文档项
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        # 获取原始内容
        content = item.get_content()
        soup = BeautifulSoup(content, 'lxml')
        
        # 示例：将所有 <p> 标签中的文本追加 " [已修改]"
        for p in soup.find_all('p'):
            if p.string:
                p.string += " [已修改]"
                
        # 将修改后的内容写回 item
        # 注意：需要编码为 bytes
        item.set_content(str(soup).encode('utf-8'))
            # 保存为新文件
    epub.write_epub(output_path, book, {})
    print(f"修改后的 EPUB 已保存: {output_path}")

# 使用示例
# modify_epub('example.epub', 'modified_example.epub')
