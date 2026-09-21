import fitz

# Path of the PDF file
input_file = r"罗马-拜占庭经济史 [上编] (厉以宁).pdf"

# Path for the output PDF file
output_file = r"罗马-拜占庭经济史 [上编] (厉以宁)2.pdf"

# Opening the PDF file and creating a handle for it
f = fitz.open(input_file)

#pages = list(range(14,15))
page = 15
dest = 2
for n in range(2):
    f.move_page(page, dest)
    page = page + 1
    dest = dest + 1

f.save(output_file)
