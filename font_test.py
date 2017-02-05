# coding=Big5
text = '中'

font = open('stdfont.24f','rb')

arraySize = 24*24

#hi = text[0]
#lo = text[1]

if lo>=161:
    font_offset = (hi - 161) * 157 + lo - 161 + 1 + 63 
    pass
else:
    font_offset = (hi - 161) * 157 + lo - 64 + 1 

if (serCode >= 472 && serCode < 5872):
    offset = (serCode - 472) * arraySize
else if (serCode >= 6281 && serCode <= 13973):
    offset = (serCode - 6281) * arraySize + 5401 * arraySize

print offset

font.seek(offset)

for x in xrange(1,24):
	line = f.read(3)
	print bin(line)
	pass


def read_char(c):
	pass