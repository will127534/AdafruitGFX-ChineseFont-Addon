# coding=Big5
import time

font = open('ascfntkc.24','rb')



arraySize = 3*24
#font.seek(942696)
count = 0
while 1:
    print count
    for x in xrange(0,24):
        line = font.read(2)
        data = int(line .encode('hex'),16)
        print bin(data)[2:].zfill(16)
        pass
    count = count +1
    time.sleep(0.01)
    pass

