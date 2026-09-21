import pymupdf

src = pymupdf.open("13个银行家（美）西蒙·约翰逊等著.pdf")
doc = pymupdf.open()  # empty output PDF

for spage in src:  # for each page in input
    r = spage.rect  # input page rectangle
    d = pymupdf.Rect(spage.cropbox_position,  # CropBox displacement if not
                  spage.cropbox_position)  # starting at (0, 0)
    page = doc.new_page(-1,  # new output page with rx dimensions
                       width = d.width,
                       height = d.height)
    page.show_pdf_page(
            page.rect,  # fill all new page with the image
            src,  # input document
            spage.number,  # input page number
            clip = d,  # which part to use of input page
        )

# that's it, save output file
doc.save("poster-" + src.name,
         garbage=3,  # eliminate duplicate objects
         deflate=True,  # compress stuff where possible
)