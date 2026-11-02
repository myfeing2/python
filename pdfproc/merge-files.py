<<<<<<< HEAD
import fitz

doc_a = fitz.open("1.png") # open the 1st document
doc_b = fitz.open("2.png") # open the 2nd document

doc_a.insert_file(doc_b) # merge the docs
doc_a.save("a+b.pdf") # save the merged document with a new filename

=======
import fitz

doc_a = fitz.open("1.png") # open the 1st document
doc_b = fitz.open("2.png") # open the 2nd document

doc_a.insert_file(doc_b) # merge the docs
doc_a.save("a+b.pdf") # save the merged document with a new filename

>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
