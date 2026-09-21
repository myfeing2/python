from pdf2image import convert_from_path


pages = convert_from_path(r'C:\Users\Lenovo\Downloads\关于北京猿人用火的证据：研究历史、争议与新进展.pdf',
                          poppler_path=r'D:\poppler-23.08.0\Library\bin')
for i in range(len(pages)):
    pages[i].save(r'img\%i.png' % i, 'PNG')
