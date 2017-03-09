# coding=Big5


font = open('font/ascfntkc.15','rb')



def printASCII(c):

    arraySize = 15
    BytePerline = 1
    size = 15
    x =  int(c[0].encode('hex'),16)
    x = 223 
    for x in xrange(0x0,0xFF):
        print x
        font.seek(x*arraySize)
      
        for y in xrange(0,size):
            line = font.read(BytePerline)
            data = int(line.encode('hex'),16)
            print bin(data)[2:].zfill(BytePerline*8)#[:-4]
        pass



def read_char(c):
    
    hi = int(c[0].encode('hex'),16)
    offset = 0
    halfwidth = 0
    arraySize = 2*15
    lo = 0
    try:
        lo = int(c[1].encode('hex'),16)
    except:
        lo = hi
        hi = 161
        halfwidth = 1
        arraySize = 2*24
        print "ASCII GET"
        return printASCII(c)

    if lo>=161:
            serCode = (hi - 161) * 157 + lo - 161 + 1 + 63 
    else:
            serCode = (hi - 161) * 157 + lo - 64 + 1 

    if (serCode >= 472) and (serCode < 5872):
        offset = (serCode - 472) * arraySize
    elif (serCode >= 6281) and (serCode <= 13973):
        offset = (serCode - 6281) * arraySize + 5401 * arraySize
        pass
    else:
        offset = serCode*arraySize
    print serCode
    print offset
    print arraySize

    font.seek(offset)
    
    if halfwidth:
        for x in xrange(0,15):
            line = font.read(2)
            data = int(line.encode('hex'),16)
            data = bin(data)[2:].zfill(24)
            print data
        pass
    else:
        for x in xrange(0,15):
            line = font.read(2)
            data = int(line .encode('hex'),16)
            print bin(data)[2:].zfill(16)
            pass
        font.seek(offset)
        for x in xrange(0,30):
            line = font.read(1)
            data = int(line .encode('hex'),16)
            print hex(data)
            pass
    


x = raw_input(">>> Input: ")
read_char(x)

