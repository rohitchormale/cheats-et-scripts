import os

#create absoute path
#eg. os.path.join(os.path.curdir,'foo')
path = os.path.join(os.path.curdir)

#list files in given folder
files = os.listdir(path)

#iterator
for file in files:
	if (os.path.splitext(file)[-1] == '.pyc'):
		continue
	print file
