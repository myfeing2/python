import fitz
from fitz import PDF_REDACT_IMAGE_NONE


def run():
    pf = r"C:\Users\Lenovo\Downloads\books\中国近现代史\杨奎松\忍不住的关怀 1949年前后的书生与政治 (杨奎松).pdf"
    doc = fitz.open(pf)
    for i in range(doc.page_count):
        page = doc.load_page(i)
        ln = page.get_links()
        print('page', i, ln, sep=' ')
        for j in ln:
            print('j')
            page.delete_link(j)

    of = r"C:\Users\Lenovo\Downloads\books\中国近现代史\杨奎松\忍不住的关怀 1949年前后的书生与政治 (杨奎松)2.pdf"
    doc.save(of)


if __name__ == '__main__':
    run()
