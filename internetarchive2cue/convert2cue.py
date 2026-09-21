
import sys, json, re, gettext

def convert2hms(ms):
    sec = int((ms/1000)%60)
    min = int((ms/(1000*60))%60)
    hms = str(min) + ':' + str(sec) + ':00'
    return hms

def convert2cue(in_file):
    with open(in_file) as f:
        ori = f.read()
        cnt = json.loads(ori)
        for item in cnt:
            ss = re.match(r'disc\d+/(.*)\.flac', item['file'])
            out_file = ss.group(1) + '.cue'
            of = open(out_file, 'w', encoding='utf-8')
            of.write('TITLE "' + item['tracks'][0]['file_md']['album'] + '"\n')
            of.write('PERFORMER "' + item['tracks'][0]['file_md']['artist'] + '"\n')
            of.write('FILE "' + ss.group(1) +'.flac" WAVE' + '\n')
            n = 1
            for track in item['tracks']:
                title = track['file_md']['title']
                index1 = convert2hms(track['segments']['final']['start'])
                of.write('  TRACK ' + str(n) + ' AUDIO\n')
                of.write('    TITLE "' + title + '"\n')
                of.write('    INDEX 01 ' + index1 + '\n')
                n = n + 1
            of.close()


if __name__ == '__main__':
    convert2cue(sys.argv[1])
