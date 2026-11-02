<<<<<<< HEAD
import fitz

doc = fitz.open(r'Foundations of Image Science by Harrison H. Barrett, Kyle J. Myers.pdf') # some new or existing PDF document
pns = [1507]
incr = 0
for pn in pns:
    npn = pn + incr
    rect = doc.load_page(npn).bound()
    page = doc.new_page(npn, # insertion point
					width = rect.width, # page dimension: A4 portrait
					height = rect.height)
    incr = incr + 1
doc.saveIncr() # save the document
=======
import fitz

doc = fitz.open(r'Foundations of Image Science by Harrison H. Barrett, Kyle J. Myers.pdf') # some new or existing PDF document
pns = [1507]
incr = 0
for pn in pns:
    npn = pn + incr
    rect = doc.load_page(npn).bound()
    page = doc.new_page(npn, # insertion point
					width = rect.width, # page dimension: A4 portrait
					height = rect.height)
    incr = incr + 1
doc.saveIncr() # save the document
>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
