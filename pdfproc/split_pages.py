import fitz


src = fitz.open(r"C:\Users\myfei\Downloads\SurveyMethodology.pdf")
doc = fitz.open()  # empty output PDF

for spage in src:  # for each page in input
    r = spage.rect  # input page rectangle
    d = fitz.Rect(spage.cropbox_position,  # CropBox displacement if not
                    spage.cropbox_position)  # starting at(0, 0)
    # --------------------------------------------------------------------------
    # example: cut input page into 2 x 2 parts
    # --------------------------------------------------------------------------
    half = round(r.width/2)
    r1 = fitz.Rect(0, 0, half-1, r.height)
    r2 = fitz.Rect(half, 0, r.width, r.height)
    '''
    if spage.number == 0:
        rect_list = [r]
    else:
        rect_list = [r1, r2]  # put them in a list
    '''

    rect_list = [r1, r2] 
    for rx in rect_list:  # run thru rect list
        rx += d  # add the CropBox displacement
        page = doc.new_page(-1,  # new output page with rx dimensions
                             width=rx.width,
                             height=rx.height)
        page.show_pdf_page(
            page.rect,  # fill all new page with the image
            src,  # input document
            spage.number,  # input page number
            clip=rx,  # which part to use of input page
        )

# that's it, save output file
doc.save(r"C:\Users\myfei\Downloads\SurveyMethodology2.pdf",
          garbage=3,  # eliminate duplicate objects
          deflate=True,  # compress stuff where possible
          )
