import re, csv

with open("out.csv",encoding='utf-8') as inf:
    with open("outupd.csv", "w", encoding='utf-8') as outf:
        tocrd = csv.reader(inf, delimiter=';')
        re_lvl1 = re.compile(r'^\d+[\.\s]')
        re_lvl2 = re.compile(r'^\d+\.\d+')
        re_lvl3 = re.compile(r'^\d+\.\d+\.\d+')
        re_lvl4 = re.compile(r'^\d+\.\d+\.\d+\.\d+')
        for row in tocrd:
            assert len(row) <= 4, "cannot handle more than 4 entries:\n %s" % (str(row),)
            # print(row[1])
            if re_lvl4.search(row[1]) != None:
                lvl = int(row[0]) + 2
            elif re_lvl3.search(row[1]) != None:
                lvl = int(row[0]) + 1
            else:
                lvl = int(row[0])
            rec = ";".join([str(lvl), row[1].strip(), row[2], row[3]])
            outf.writelines([rec, "\n"])
