<<<<<<< HEAD
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

=======
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

>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
