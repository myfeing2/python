from PIL import Image
# import os
import glob

imagedir = r"C:\Users\myfei\Downloads\赢在美国\\"
# imageFileList = [imagedir + line[:-1] for line in os.popen(f'dir {imagedir}*.* /B /ON').readlines()]
imageFileList = glob.glob(imagedir+'*')
# print(imageFileList)
imageObjectList = [Image.open(imageFile) for imageFile in imageFileList]
imageList = [imageItem.convert('RGB') for imageItem in imageObjectList]
# print(imageList)
imageList[0].save(r'C:\Users\myfei\Downloads\赢在美国.pdf', save_all=True, append_images=imageList[1:], optimize=True)
