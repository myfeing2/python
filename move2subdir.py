import sys, os, shutil
import re, glob

def lister(root):
    last_subdir = ""
    p = re.compile(r'([AB]\d\d_*)(\d{2,3}_)([a-zA-Z0-9]+)_*(ENGESVC2DA\.mp3)$')
    for fpath in glob.glob(root + r"\*.mp3"):
        # path = os.path.join(thisdir, fname)
        dir, fname = os.path.split(fpath)
        #print(fname)
        m = p.match(fname)
        print(m)
        if m :
            curr_subdir = dir + '\\' + m.group(1) + m.group(3)
        else :
            raise Exception("No file found")
        print('curr_dir: ' + curr_subdir)
        if last_subdir == curr_subdir :
            shutil.move(fpath, curr_subdir)
        else:
            last_subdir = curr_subdir
            if os.path.isdir('curr_subdir'):
                os.makedirs(curr_subdir)
            shutil.move(fpath, curr_subdir)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lister(sys.argv[1])
