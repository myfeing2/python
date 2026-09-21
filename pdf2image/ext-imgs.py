import fitz

doc = fitz.open(r'C:\Users\Lenovo\Downloads\周口店第 1 地点用火的磁化率和色度证据.pdf')  # open a document

for page_index in range(len(doc)):  # iterate over pdf pages
    page = doc[page_index]  # get the page
    image_list = page.get_images()

    # print the number of images found on the page
    if image_list:
        print(f"Found {len (image_list)} images on page {page_index}")
    else:
        print("No images found on page", page_index)

    for image_index, img in enumerate(image_list, start=1):  # enumerate the image list
        xref = img[0]  # get the XREF of the image
        pix = fitz.Pixmap(doc, xref)  # create a Pixmap

        if pix.n - pix.alpha > 3:  # CMYK: convert to RGB first
            pix = fitz.Pixmap(fitz.csRGB, pix)

        pix.save(r"img\page_%s-image_%s.png" % (page_index, image_index))  # save the image as png
        pix = None
