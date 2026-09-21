import os
from PIL import Image


indir = r"imgs\\"
outdir = r"imgs-out\\"
infilenamelist = [line[:-1] for line in os.popen(f'dir {indir}*.* /B').readlines()]
for infilename in infilenamelist:
    infile = indir + infilename
    with Image.open(infile) as im:
        w = round(im.width/2)
        box1 = (38, 291, 738, 966)
        region1 = im.crop(box1)
        # print(infile, im.format, f"{im.size}x{im.mode}")
        im1 = Image.new('RGBA', (box1[2], box1[3]))
        im1.paste(region1)
        #print(outfile1)
        im1.save(outdir+infilename)
