import fitz
from fitz import PDF_REDACT_IMAGE_NONE

text = '好书天天看'


def run():
    pf = r"C:\Users\Lenovo\Downloads\books\中国近现代史\杨奎松\忍不住的关怀 1949年前后的书生与政治 (杨奎松)2.pdf"
    doc = fitz.open(pf)
    for i in range(doc.page_count):
        page = doc.load_page(i)
        rl = page.search_for(text, quads=True)
        page.add_redact_annot(rl[0])
        page.apply_redactions(images=PDF_REDACT_IMAGE_NONE)

    of = r"C:\Users\Lenovo\Downloads\books\中国近现代史\杨奎松\忍不住的关怀 1949年前后的书生与政治 (杨奎松)3.pdf"
    doc.save(of)


if __name__ == '__main__':
    run()
