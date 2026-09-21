from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  
  
import glob
import re
import sys, os

# extract the file names (with file paths)  
filez = glob.glob(sys.argv[1] + r"\*.mp3", recursive=True)
# print(filez)
for i in range(0, len (filez)):  
	# mp3 name (with directory) from filez  
    song = filez[i]
    # print(song)
	# turn it into an mp3 object using the mutagen library  
    mp3file = MP3(song, ID3=EasyID3)  
	# set the album name  
	# mp3file['album'] = ['Punk-O-Rama Vol. 1 (1994)']  
	# set the albumartist name  
	# mp3file['albumartist'] = ['Punk-O-Rama Vol. 1']  
	# set the track number with the proper format  
	# mp3file['tracknumber'] = str(tracknum) + '/' + str(len(filez))  
    tt = mp3file['title'][0]
    tr = re.compile(r'/')
    tt1 = tr.sub('-', tt)
    # print(tt1)
    ntt = mp3file['tracknumber'][0] + ". " + tt1
    nfn = os.path.dirname(filez[i]) + "\\" + ntt + ".mp3"
    # print(nfn)
    os.rename(filez[i], nfn)
	# save the changes that we've made  
    # mp3file.save()
    
