# (Minimal) Perfect Hash Functions Generator (key, value) value in this code is the key counter during reading but can be any number

# implementing the MOS Algorithm II CACM92 , and Amjad M Daoud Thesis 1993 at VT; 
# based on Steve Hanof implementation http://stevehanov.ca/blog/index.php?id=119.

# Download as http://iswsa.acm.org/mphf/mphf.py

# You need Python; runs linearly even on a Android phone; it runs without modifications at http://www.compileonline.com/execute_python_online.php

# For minimal perfect hashing use:  size = len(dict)

import sys

import math
font = open('stdfont.24f','rb')
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
	font_output.write('uint32_t hash(uint32_t d,uint8_t* str,int len){\n	if (d == 0)\n		d = 0x811C9DC5UL;\n	for (int i = 0; i < len; ++i)\n	{\n		d = d ^ (uint32_t)str[i] * 16777619 & 0xffffffff;\n	}\n	return d;\n}\nuint32_t lookup(uint8_t* str,int len){\n	unsigned long d = g[hash(0,str,len) % g_size];\n	if (d<0)\n		return V[-d-1];\n	return V[hash(d,str,len) % V_size];\n}\n')

	pass


arraySize = 3*24
def font_to_code(c):
	font_output.write('const unsigned char user_font[]  = {')

	for x in xrange(0,72):
		font_output.write(hex(0x00)+', ')
	font_output.write('\n')
	length = 0
	for x in c:
		read_char(x)
		length +=1
		pass
	font_output.seek(font_output.tell()-1)
	font_output.write('};\n')
	font_output.write('const GFXglyph user_fontGlyphs[]  = {\n')
	font_output.write("{     0,  0,  0,  24,   0,   0 },\n")
	for x in xrange(0,length):
		font_output.write("{     %d,  24,  24,  24,   0,   0 },\n" % ((x+1)*72))
		pass
	font_output.seek(font_output.tell()-1)
	font_output.write('};\n')


	font_output.write("const GFXfont user_fontGFXfont PROGMEM = {\n  (uint8_t  *)user_font,\n  (GFXglyph *)user_fontGlyphs,\n  0x00, 0xFFFFFFUL, 30};\n")

	pass

def read_char(c):
    
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

    #print offset

    font.seek(offset)

    for x in xrange(1,24):
        line = font.read(3)
        data = int(line .encode('hex'),16)
        #print bin(data)[2:].zfill(24)
        pass
    font.seek(offset)
    for x in xrange(0,72):
        data = int(font.read(1).encode('hex'),16)
        font_output.write(hex(data)+', ')
    font_output.write('\n')


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
	test.append(x.decode('utf-8').encode('big5'))
	pass
font_to_code(test)