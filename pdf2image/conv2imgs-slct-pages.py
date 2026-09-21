import fitz

doc = fitz.open(r'低端人口：中國，是地下這幫鼠族撐起來的.pdf')  # open a document
pages = [0, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28]
for page_index in pages:  # iterate over pdf pages
    page = doc[page_index]  # get the page
    pix = page.get_pixmap()
    pix.save(r"imgs\page_%s.png" % page_index)  # save the image as png
    pix = None
