import os, fitz
# import PySimpleGUI as psg  # for showing a progress bar

doc = fitz.open()  # PDF with the pictures
imgdir = r"imgs"  # where the pics are
# uidir = unicode(imgdir,'utf-8')
imglist = os.listdir(imgdir)  # list of them
imgcount = len(imglist)  # pic count

for i, f in enumerate(imglist):
    img = fitz.open(os.path.join(imgdir, f))  # open pic as document
    rect = img[0].rect  # pic dimension
    pdfbytes = img.convert_to_pdf()  # make a PDF stream
    img.close()  # no longer needed
    imgPDF = fitz.open("pdf", pdfbytes)  # open stream as PDF
    page = doc.new_page(width = rect.width,  # new page with ...
                       height = rect.height)  # pic dimension
    page.show_pdf_page(rect, imgPDF, 0)  # image fills the page
    # psg.EasyProgressMeter("Import Images",  # show our progress
    #    i+1, imgcount)

doc.save(r"i.pdf")
