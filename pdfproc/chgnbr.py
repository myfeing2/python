<<<<<<< HEAD
import fitz

fname = r"牛津政治行为研究手册（下册）.pdf"
doc = fitz.open(fname)
doc.set_page_labels([{'startpage':0, 'prefix':'', 'style':'R','firstpagenum':1},
    {'startpage':11, 'prefix':'', 'style':'D','firstpagenum':416}])
of = r'牛津政治行为研究手册（下册）2.pdf'
doc.save(of)
=======
import fitz

fname = r"牛津政治行为研究手册（下册）.pdf"
doc = fitz.open(fname)
doc.set_page_labels([{'startpage':0, 'prefix':'', 'style':'R','firstpagenum':1},
    {'startpage':11, 'prefix':'', 'style':'D','firstpagenum':416}])
of = r'牛津政治行为研究手册（下册）2.pdf'
doc.save(of)
>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
