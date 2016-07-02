import sys
import csv
from os import listdir, rename, path
from shutil import copyfile

src = sys.argv[1]
dst = sys.argv[2]
dst_file = 'samples.csv'

files = [f for f in listdir(src) if f.find('.png') > 0]

with open(dst + '/' + dst_file, 'wb') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    idx = 0
    for f in files:
        basename, ext = path.splitext(path.basename(f))
        id_ = basename
        new_f = '%03d%s' % (idx, ext)
        writer.writerow([new_f, id_])
        copyfile(src + '/' + f, dst + '/' + new_f)
        idx += 1


