<<<<<<< HEAD
from sys import argv
import fitz, os

# mat = fitz.Matrix(500, 500)
doc = fitz.open(argv[1])  # open a document
page = doc.load_page(int(argv[2]))
pix = page.get_pixmap(dpi=1200)
pix.save("page-%i.png" % page.number)
=======
from sys import argv
import fitz, os

# mat = fitz.Matrix(500, 500)
doc = fitz.open(argv[1])  # open a document
page = doc.load_page(int(argv[2]))
pix = page.get_pixmap(dpi=1200)
pix.save("page-%i.png" % page.number)
>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
