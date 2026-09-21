import fitz

# Path of the PDF file
input_file = r"C:\Users\Lenovo\Downloads\psychiatry\精神病学史：从收容院到百忧解.pdf"

# Path for the output PDF file
output_file = r"C:\Users\Lenovo\Downloads\psychiatry\精神病学史：从收容院到百忧解2.pdf"

# Opening the PDF file and creating a handle for it
f = fitz.open(input_file)
f.move_page(1, 0)
f.save(output_file)
