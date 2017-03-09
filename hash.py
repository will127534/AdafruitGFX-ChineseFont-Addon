import sys
from optparse import OptionParser
import math

font_output = open('userfont.h','w')

# first level simple hash ... used to disperse patterns using random d values

def hash( d, str ):

    #if d == 0: d = 0x01000193

    if d == 0: d =   0x811C9DC5

    # Use the FNV-1a hash

    for c in str:
        #h = (h ^ p[i]) * 16777619
        #d = ( (d * 0x01000193) ^ ord(c) ) & 0xffffffff;
        d = d ^ int(c.encode('hex'),16) * 16777619 & 0xffffffff

    return d 

def isprime(x):

    x = abs(int(x))

    if x < 2:

        return "Less 2", False

    elif x == 2:

        return True

    elif x % 2 == 0:

        return False    

    else:

        for n in range(3, int(x**0.5)+2, 2):

            if x % n == 0:

                return False

        return True

def nextprime(x):

    while ( True ):

       if isprime(x): break

       x += 1

    return x  

# create PHF with MOS(Map,Order,Search), g is specifications array

def CreatePHF( dict ):

    size = len(dict) 

    size = nextprime(len(dict)+len(dict)/4)

    print "Size = %d" % (size)

    #nextprime(int(size/(6*math.log(size,2)))) 
    #c=4 corresponds to 4 bits/key
    # for fast construction use size/5
    # for faster construction use gsize=size
    gsize = size/5 

    print "G array size = %d" % (gsize)

    sys.stdout.flush()

 

    #Step 1: Mapping

    patterns = [ [] for i in range(gsize) ]

    g = [0] * gsize #initialize g

    values = [None] * size #initialize values

    

    for key in dict.keys():

        patterns[hash(0, key) % gsize].append( key )

 

    # Step 2: Sort patterns in descending order and process 

    patterns.sort( key= len, reverse=True )        

    for b in xrange( gsize ):

        pattern = patterns[b]

        if len(pattern) <= 1: break

        

        d = 1

        item = 0

        slots = []

 

    # Step 3: rotate patterns and search for suitable displacement

        while item < len(pattern):

            slot = hash( d, pattern[item] ) % size

            if values[slot] != None or slot in slots:

                d += 1

                if d < 0 : break

                item = 0

                slots = []

            else:

                slots.append( slot )

                item += 1

 

        if d < 0: 

           print "failed"

           return

           

        g[hash(0, pattern[0]) % gsize] = d

        for i in range(len(pattern)):

            values[slots[i]] = dict[pattern[i]]

 

        if ( b % 100 ) == 0:

           print "%d: pattern %d processed" % (b,len(pattern))

           sys.stdout.flush()

 

    # Process patterns with one key and use a negative value of d 

    freelist = []

    for i in xrange(size): 

        if values[i] == None: freelist.append( i )

 

    for b in xrange(b+1,gsize ):

        pattern = patterns[b]

        if len(pattern) == 0: break

        #if len(pattern) > 1: continue;

        slot = freelist.pop()

        # subtract one to handle slot zero

        g[hash(0, pattern[0]) % gsize] = -slot-1 

        values[slot] = dict[pattern[0]]

        

        if (b % 1000) == 0:

           print "-%d: pattern %d processed" % (b,len(pattern))

           sys.stdout.flush()

    print "PHF succeeded"

    return (g, values)        

# Look up a value in the hash table, defined by g and V.

def lookup( g, V, key ):

    d = g[hash(0,key) % len(g)]
    if d < 0: return V[-d-1]
    return V[hash(d, key) % len(V)]

def print_hash_function(g,V):
    font_output.write('#define V_size ' + str(len(V))+'\n')
    font_output.write('#define g_size ' + str(len(g))+'\n')
    font_output.write('const int g[] = {')
    lenght = len(g)
    for x in xrange(0,lenght-1):
        font_output.write(str(g[x])+', ')
        pass
    font_output.write(str(g[lenght-1])+'};\n')


    font_output.write('const int V[] = {')
    lenght = len(V)
    for x in xrange(0,lenght-1):
        if V[x] == None:
            font_output.write('NULL, ')
            pass
        else:
            font_output.write(str(V[x])+', ')
        pass
    font_output.write(str(V[lenght-1])+'};\n')
    font_output.write('uint32_t hash(uint32_t d,uint8_t* str,int len){\n    if (d == 0)\n       d = 0x811C9DC5UL;\n for (int i = 0; i < len; ++i)\n {\n     d = d ^ (uint32_t)str[i] * 16777619 & 0xffffffff;\n }\n return d;\n}\nuint32_t lookup(uint8_t* str,int len){\n  unsigned long d = g[hash(0,str,len) % g_size];\n    if (d<0)\n      return V[-d-1];\n   return V[hash(d,str,len) % V_size]+95;\n}\n')

    pass


def write_ascii(font_ASCII,size):
    if size == 24:
        arraySize = 48
        BytePerline = 2
        pass
    if size == 15:
        arraySize = 15
        BytePerline = 1
        pass

    for x in xrange(0x20,0x80):

        if debug:
            font_ASCII.seek(x*arraySize)

            for y in xrange(0,size):
                line = font_ASCII.read(BytePerline)
                data = int(line.encode('hex'),16)
                print bin(data)[2:].zfill(BytePerline*8)#[:-4]

        font_ASCII.seek(x*arraySize)

        for y in xrange(0,arraySize):
            line = font_ASCII.read(1)
            data = int(line.encode('hex'),16)
            font_output.write(hex(data)+', ')
        
        font_output.write('\n')
        pass
    pass


def font_to_code(c,size):

    if size == 15:
        font = open('font/stdfont.15f','rb')
        font_ASCII = open('font/ascfntkc.15','rb')
        arraySize = 30
        BytePerline = 2
        arraySize_ASCII = 15
        pass
    if size == 24:
        font = open('font/stdfont.24f','rb')
        font_ASCII = open('font/ascfntkc.24','rb')
        arraySize = 72
        BytePerline = 3
        arraySize_ASCII = 48
        pass

    font_output.write('const unsigned char user_font[]  = {')

    write_ascii(font_ASCII,size)

    length = 0
    for x in c:
        read_char(x,font,size)
        length +=1
        pass
    font_output.seek(font_output.tell()-1)
    font_output.write('};\n')
    font_output.write('const GFXglyph user_fontGlyphs[]  = {\n')

    if size == 15:
        width = 16
        hight = 15
        width_ASCII = 8
        hight_ASCII = 15
        halfwidth = 8
        pass
    if size == 24:
        width = 24
        hight = 24
        width_ASCII = 16
        hight_ASCII = 24
        halfwidth = 12
        pass

    for x in xrange(0x20,0x80):
        
        font_output.write("{     %d,  %d,  %d,  %d,   0,   0 },\n" % ((x-0x20)*arraySize_ASCII,width_ASCII,hight_ASCII,halfwidth))
        pass

    for x in xrange(0,length):

        font_output.write("{     %d,  %d,  %d,  %d,   0,   0 },\n" % ((x)*arraySize+(0x7E-0x20+2)*arraySize_ASCII,width,hight,width))
        pass
    font_output.seek(font_output.tell()-1)
    font_output.write('};\n')


    font_output.write("const GFXfont user_fontGFXfont PROGMEM = {\n  (uint8_t  *)user_font,\n  (GFXglyph *)user_fontGlyphs,\n  0x20, 0xFFFFFFUL, %d};\n" % int(hight*1.25))

    pass


def read_char(c,font,size):

    if size == 24:
        arraySize = 72
        BytePerline = 3
        pass
    if size == 15:
        arraySize = 30
        BytePerline = 2
        pass

    offset = 0
    hi = int(c[0].encode('hex'),16)
    lo = int(c[1].encode('hex'),16)

    if lo>=161:
        serCode = (hi - 161) * 157 + lo - 161 + 1 + 63 
    else:
        serCode = (hi - 161) * 157 + lo - 64 + 1 
    if serCode >= 472 & serCode < 5872:
        offset = (serCode - 472) * arraySize
    elif serCode >= 6281 & serCode <= 13973:
        offset = (serCode - 6281) * arraySize + 5401 * arraySize
        pass
    if debug:
        font.seek(offset)
        for x in xrange(0,size):
            line = font.read(BytePerline)
            data = int(line .encode('hex'),16)
            print bin(data)[2:].zfill(BytePerline*8)
            pass

    font.seek(offset)
    for x in xrange(0,arraySize):
        data = int(font.read(1).encode('hex'),16)
        font_output.write(hex(data)+', ')
    font_output.write('\n')
    

parser = OptionParser(usage="python %prog [options]")
parser.add_option("-s", action="store_true",dest="Small", help="Small Font")
parser.add_option("-p", action="store_true",dest="debug", help="print Font")

(opt, args) = parser.parse_args()
debug = opt.debug
size = 24
if opt.Small:
    size = 15
    pass


print "Reading dict words"

dict = {}

line = 1
for key in open('discrete.txt', "rt").readlines():
    dict[key.strip()] = line
    line +=1
 
#creating phf

print "Creating perfect hash"
print dict
(g, V) = CreatePHF( dict )


#printing phf specification

print "Printing g[]"

print g
print V

print_hash_function(g,V)

test = []
for x in open('discrete.txt', "rt").readlines():
    test.append(x.strip('\n').strip('\r').decode('utf-8').encode('big5'))
    pass

font_to_code(test,size)

#fast verification for few (key,value) count given by num1
'''
num1 = line

print "Verifying hash values for the first %d words"% (num1)


for key in open('discrete.txt', "rt").readlines():

    line = lookup( g, V, key.strip() )

    print "Word %s occurs on line %d" % (key.strip(), line)

    line += 1

    if line > num1: break
    '''