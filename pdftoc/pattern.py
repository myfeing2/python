import re, csv


with open("in.txt",encoding='utf-8') as inf:
    with open("in.csv", "w", encoding='utf-8') as outf:
        cw = csv.writer(outf, delimiter =';',quotechar ='"',lineterminator='\n',quoting=csv.QUOTE_NONNUMERIC)
        re_title = re.compile(r'^(.*)(?<=\s)(\d+)$')
        from_lvl0 = 0
        re_lvl0 = re.compile(r'^[^\d]+')
        re_lvl1 = re.compile(r'^([^\d]+|\d+[\.\s])')
        re_lvl2 = re.compile(r'^(\d+\.\d+)')
        re_lvl3 = re.compile(r'^\d+\.\d+\.\d+')
        re_lvl4 = re.compile(r'^\d+\.\d+\.\d+\.\d+')
        re_div = re.compile(r'(?<=\d[\.\s]|[^\d]\s)\s*((\.\s?)+(?=\d))')
        tot_lines = inf.readlines()
        lvl = 1
        for line in  tot_lines:
            
            if from_lvl0 != 0 and re_div.search(line) != None:
                sline = re_div.sub(' ', line)
            else:
                sline = line
            
            # print(sline)
            # print(sline)
            mat_title = re_title.search(sline)
            # print(mat_title.groups())
            if tot_lines.index(line) > 2:
                pn = str(int(mat_title.group(2).strip()) + 14)
            else:
                pn = mat_title.group(2).strip()
            # pn = str(int(mat_title.group(2).strip()) + 21)
            if re_lvl4.search(sline) != None:
                lvl = 4 + from_lvl0
            elif re_lvl3.search(sline) != None:
                lvl = 3 + from_lvl0
            elif re_lvl2.search(sline) != None:
                lvl = 2 + from_lvl0
            elif re_lvl1.search(sline) != None:
                lvl = 1 + from_lvl0
            elif from_lvl0 != 0:
                lvl = from_lvl0
            newline = [lvl, mat_title.group(1).strip(), int(pn)]
            # print(newline)
            cw.writerow(newline)

