from pikepdf import Pdf, PdfImage, Name

example = Pdf.open(r'C:\Users\Lenovo\Downloads\books\中国近现代史\杨奎松\忍不住的关怀 1949年前后的书生与政治 (杨奎松).pdf')

page = example.pages[0]
list(page.images.keys())
rawimage = page.images['/Im0']  # The raw object/dictionary
pdfimage = PdfImage(rawimage)
pdfimage.extract_to(fileprefix='image')
