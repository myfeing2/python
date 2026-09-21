import fitz

path = r""

# Path of the PDF file
input_file = path + r"13个银行家（美）西蒙·约翰逊等著.pdf"

# Path for the output PDF file
# output_file = path + r"Foundations of Image Science by Harrison H. Barrett, Kyle J. Myers2.pdf"

# Opening the PDF file and creating a handle for it
file_handle = fitz.open(input_file)

# This list contains the pages that we are willing to keep
# Rest are deleted
# pages_list = [5]

# Passing the list to the select function

file_handle.delete_page(255)
file_handle.delete_pages(5, 6)

# Saving the file
file_handle.saveIncr()
