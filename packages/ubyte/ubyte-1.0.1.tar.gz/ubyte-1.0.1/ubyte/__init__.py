import numpy as np
import struct
from datetime import datetime
import sys



# decode idx3-ubyte files
def decode_idx3_ubyte(fileDir):
    print('Getting platform type...')
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        fileName = fileDir.split('\\')[-1]
        os = 'windows'
    else:
        fileName = fileDir.split('/')[-1]
        os = 'unix-type system'
    print('Your computer\'s platform type is %s .' % os)
    
    
    startTime = datetime.now()
    start = float(startTime.strftime('%H'))*3600 + float(startTime.strftime('%M'))*60 + float(startTime.strftime('%S')) + float(startTime.strftime('%f')) / 1000000
    print('Start decoding %s (the complete directory is %s.)' % (fileName,fileDir))
    
    
    print('Opening %s .' % fileName)
    
    bin_data = open(fileDir, 'rb').read()
    
    breakTime = datetime.now()
    _break = float(breakTime.strftime('%H'))*3600 + float(breakTime.strftime('%M'))*60 + float(breakTime.strftime('%S')) + float(breakTime.strftime('%f')) / 1000000
    print(' Successfully opened %s,used time %f s.'%(fileName,_break - start))
    del _break,breakTime
    
    
    print('Decoding header information .')
    
    offset = 0
    fmt_header = '>iiii'
    magic_number, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, bin_data, offset)
    print(' Magic number: %d,number of images: %d,size of images: %d*%d.' % (magic_number, num_images, num_rows, num_cols))
    
    breakTime = datetime.now()
    _break = float(breakTime.strftime('%H'))*3600 + float(breakTime.strftime('%M'))*60 + float(breakTime.strftime('%S')) + float(breakTime.strftime('%f')) / 1000000
    print(' Successfully decoded header information,used time %f s.' % (_break - start))
    del _break,breakTime
    
    
    print('Decoding main part.')
    
    image_size = num_rows * num_cols
    offset += struct.calcsize(fmt_header)
    fmt_image = '>' + str(image_size) + 'B'
    images = np.empty((num_images, num_rows, num_cols))
    for i in range(num_images):
        nowTime = datetime.now()
        now = float(nowTime.strftime('%H'))*3600 +float(nowTime.strftime('%M'))*60 +float(nowTime.strftime('%S')) +float(nowTime.strftime('%f')) / 1000000
        usedTime = float(now - start)
        if ((usedTime) * 10) % 1 <= 0.00025:
            print(' Decoded %d sheets,used time %f s,etc %f s.' % (i + 1,usedTime,(num_images - i + 1)*(usedTime / (i + 1))))
        images[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows, num_cols))
        offset += struct.calcsize(fmt_image)
    
    breakTime = datetime.now()
    _break = float(breakTime.strftime('%H'))*3600 + float(breakTime.strftime('%M'))*60 + float(breakTime.strftime('%S')) + float(breakTime.strftime('%f')) / 1000000
    print(' Successfully decoded main part,used time %f s.' % (_break - start))
    
    
    doneTime = datetime.now()
    done = float(doneTime.strftime('%H'))*3600 + float(doneTime.strftime('%M'))*60 + float(doneTime.strftime('%S')) + float(doneTime.strftime('%f')) / 1000000
    print('Successfully decoded %s,used time %f s.' % (fileName,done - start))
    return images



# decode idx1-ubyte files
def decode_idx1_ubyte(fileDir):
    print('Getting platform type...')
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        fileName = fileDir.split('\\')[-1]
        os = 'windows'
    else:
        fileName = fileDir.split('/')[-1]
        os = 'unix-type system'
    print('Your computer\'s platform type is %s .' % os)
    
    
    startTime = datetime.now()
    start = float(startTime.strftime('%H'))*3600 + float(startTime.strftime('%M'))*60 + float(startTime.strftime('%S')) + float(startTime.strftime('%f')) / 1000000
    print('Start decoding %s (the complete directory is %s.)' % (fileName,fileDir))
    
    
    print('Opening %s.' % fileName)
    
    bin_data = open(fileDir, 'rb').read()
    
    breakTime = datetime.now()
    _break = float(breakTime.strftime('%H'))*3600 + float(breakTime.strftime('%M'))*60 + float(breakTime.strftime('%S')) + float(breakTime.strftime('%f')) / 1000000
    print(' Successfully decoded header information,used time %f s.' % (_break - start))
    del _break,breakTime
    
    
    print('Decoding header information.')
    
    offset = 0
    fmt_header = '>ii'
    magic_number, num_images = struct.unpack_from(fmt_header, bin_data, offset)
    print (' Magic number: %d,number of images: %d.' % (magic_number, num_images))
    
    breakTime = datetime.now()
    _break = float(breakTime.strftime('%H'))*3600 + float(breakTime.strftime('%M'))*60 + float(breakTime.strftime('%S')) + float(breakTime.strftime('%f')) / 1000000
    print(' Successfully decoded header information,used time %f s.' % (_break - start))
    del _break,breakTime
    
    
    print('Decoding main part.')
    
    offset += struct.calcsize(fmt_header)
    fmt_image = '>B'
    labels = np.empty(num_images)
    for i in range(num_images):
        nowTime = datetime.now()
        now = float(nowTime.strftime('%H'))*3600 +float(nowTime.strftime('%M'))*60 +float(nowTime.strftime('%S')) +float(nowTime.strftime('%f')) / 1000000
        usedTime = float(now - start)
        if ((usedTime) * 10) % 1 <= 0.00025:
            print(' Decoded %d sheets,used time %f s,etc %f s.' % (i + 1,usedTime,(num_images - i + 1)*(usedTime / (i + 1))))
        labels[i] = struct.unpack_from(fmt_image, bin_data, offset)[0]
        offset += struct.calcsize(fmt_image)
    
    breakTime = datetime.now()
    _break = float(breakTime.strftime('%H'))*3600 + float(breakTime.strftime('%M'))*60 + float(breakTime.strftime('%S')) + float(breakTime.strftime('%f')) / 1000000
    print(' Successfully decoded main part,used time %f s.' % (_break - start))
    
    
    doneTime = datetime.now()
    done = float(doneTime.strftime('%H'))*3600 + float(doneTime.strftime('%M'))*60 + float(doneTime.strftime('%S')) + float(doneTime.strftime('%f')) / 1000000
    print('Successfully decoded %s,used time %f s.' % (fileName,done - start))
    return labels
