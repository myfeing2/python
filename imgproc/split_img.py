import os
from PIL import Image


indir = r"D:\myproj\python\img\\"
outdir = r"D:\myproj\python\img2\\"
infilenamelist = [line[:-1] for line in os.popen(f'dir {indir}*.* /B').readlines()]
for infilename in infilenamelist:
    infile = indir + infilename
    with Image.open(infile) as im:
        w = round(im.width/2)
        box1 = (0, 0, w-1, im.height)
        box2 = (w, 0, im.width, im.height)
        print(box1, box2, sep=' ')
        region1 = im.crop(box1)
        region2 = im.crop(box2)
        # print(infile, im.format, f"{im.size}x{im.mode}")
        im1 = Image.new('RGBA', (box1[2], box1[3]))
        im1.paste(region1)
        outfile1 = infilename[0:16] + '1' + infilename[-4:]
        print(outfile1)
        im1.save(outdir+outfile1)
        im2 = Image.new('RGBA', (region2.width, region2.height))
        im2.paste(region2)
        outfile2 = infilename[0:16] + '2' + infilename[-4:]
        im2.save(outdir+outfile2)
