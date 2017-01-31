import sys

f = open(sys.argv[1],'r')

data = f.readlines()

discrete_char_set = []

for line in data:
	print line
	charlist = line.strip('\n').decode('utf-8')
	for char in charlist:
		if not char in discrete_char_set:
			discrete_char_set.append(char)
			pass
		pass
	pass

print discrete_char_set
print "Count:"+str(len(discrete_char_set))
f = open('discrete.txt','w')

for x in xrange(1,len(discrete_char_set)-1):
	f.write(discrete_char_set[x].encode('utf-8')+'\n')
	pass
f.write(discrete_char_set[len(discrete_char_set)-1].encode('utf-8'))