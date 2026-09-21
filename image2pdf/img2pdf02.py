from PIL import Image
import os

imagedir = r"E:\乐谱\人间"
# imageFileList = [imagedir + line[:-1] for line in os.popen(f'dir {imagedir}\\*.* /B').readlines()]
imageFileList = []
for i in range(421):
    imageFileList = imageFileList + [imagedir + '\\' + str(i) + '.png']
print(imageFileList)

imageObjectList = [Image.open(imageFile) for imageFile in imageFileList]
imageList = [imageItem.convert('RGB') for imageItem in imageObjectList]
imageList[0].save(r'out.pdf', save_all=True, append_images=imageList[1:], optimize=True)
