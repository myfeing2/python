import fitz


def run():
    pf = r"C:\Users\myfei\Downloads\Incompleteness - The Proof and Paradox of Kurt Godel by Rebecca Goldstein（2005）.pdf"
    doc = fitz.open(pf)
    of = r"C:\Users\myfei\Downloads\Incompleteness - The Proof and Paradox of Kurt Godel by Rebecca Goldstein（2005）2.pdf"
    out = fitz.open()
    ori_cnt = doc.page_count
    for i in range(doc.page_count):
        page = doc[i]
        if i == -1:
            doc.fullcopy_page(i)
        else:
            #rect = page.rect
            #rect2 = fitz.paper_rect('A5')
            page.set_cropbox(fitz.Rect(144, 32, 462, 624))
            page2 = out.new_page() #(width=rect2.width, height=rect2.height)
            page2.show_pdf_page(page2.rect, doc, i, keep_proportion=True)
            # page.set_mediabox(page.mediabox)
            #rect3 = fitz.Rect(round(rect.y1/2, 3), rect.y0, rect.y1, rect.x1)
            #doc.fullcopy_page(i)

    #doc.delete_pages(0, ori_cnt)
    out.save(of)


if __name__ == '__main__':
    run()
