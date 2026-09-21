import fitz


dir = r"C:\Users\myfei\Downloads\国际风险与保险：环境---管理分析(下册)\\"
files = ["01","02","03","04","05","06","07","08",
         "09","10",
         "11","12","13","14","15","16","17","18",
         "19","20","21","22","23","24","25","26",
         "27","28","29"]
paths = [dir + f + ".pdf" for f in files]
docs = [fitz.open(f) for f in paths] 

doc_a = docs[0]
pn = doc_a.page_count
toc = doc_a.get_toc()
for d in docs[1:]:
    doc_a.insert_pdf(d) # merge the docs
    tt = d.get_toc()
    for t in tt:
        t[2] = t[2] + pn
    toc = toc + tt
    pn = pn + d.page_count


doc_a.set_toc(toc)
doc_a.save("output.pdf") # save the merged document with a new filename

