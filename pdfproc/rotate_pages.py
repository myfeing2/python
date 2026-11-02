<<<<<<< HEAD
import fitz


def run():
    pf = r"C:\Users\myfei\Downloads\运动解剖学图谱（第2版).pdf"
    doc = fitz.open(pf)
    for i in range(doc.page_count):
        page = doc.load_page(i)
        page.set_rotation(-90)

    of = r"C:\Users\myfei\Downloads\运动解剖学图谱（第2版)2.pdf"
    doc.save(of)


if __name__ == '__main__':
    run()
=======
import fitz


def run():
    pf = r"C:\Users\myfei\Downloads\运动解剖学图谱（第2版).pdf"
    doc = fitz.open(pf)
    for i in range(doc.page_count):
        page = doc.load_page(i)
        page.set_rotation(-90)

    of = r"C:\Users\myfei\Downloads\运动解剖学图谱（第2版)2.pdf"
    doc.save(of)


if __name__ == '__main__':
    run()
>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
