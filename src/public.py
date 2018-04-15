import os

def EnsureDir(filepath):
	directory = os.path.dirname(filepath)
	print filepath
	print directory
	if not os.path.exists(directory):
		print "creando directorio", directory
		os.makedirs(directory)