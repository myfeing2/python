import pdfplumber

pdf = pdfplumber.open("sl.pdf")
# all_images = []


# for page in pdf.pages:
#     for image in page.images:
#         all_images.append({**image, **{"page_number": page.page_number}}

page = pdf.pages[4]
images = page.images
print(images.keys())
print('===============')
print(images)
print('===============')
print(images[0])
print('===============')
print(images[1])

