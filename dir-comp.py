import sys, os

def printdiff(cdir, diff):
    print(cdir+":\n\t")
    print(diff)
    print("\n")

def writediff(cdir, diff, fp):
    fp.write(cdir)
    fp.write(":\n\t")
    fp.write(str(diff))
    fp.write("\n\n")

def mylister(currdir, tardir, fp):
    #print('[' + currdir + ']')
    currset = set(os.listdir(currdir))
    if not os.path.isdir(tardir):
        printdiff(currdir, set())
        writediff(currdir, {"not in "+tardir}, fp)
    else:
        tarset = set(os.listdir(tardir))
        diff = currset.difference(tarset)
        if diff != set():
            printdiff(currdir, diff)
            writediff(currdir, diff, fp)
        diff2 = tarset.difference(currset)
        if diff2 != set():
            printdiff(tardir, diff2)
            writediff(tardir, diff2, fp)
        for file in os.listdir(currdir): # list files here
            path = os.path.join(currdir, file) # add dir path back
            if os.path.isdir(path):
                tarpath = os.path.join(tardir, file)
                mylister(path, tarpath, fp) # recur into subdirs

if __name__ == '__main__':
    with open(sys.argv[3], "w", encoding="utf-8") as fp:
        mylister(sys.argv[1], sys.argv[2], fp) # dir name in cmdlin
