import csv

def Transform(filenamein='output.txt', filenameout='output.csv'):
	with open(filenamein,'r') as f:
		content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	seconds = 0
	with open(filenameout, 'w') as f:
		fieldnames = ['direction','seconds','speak']
		writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
		writer.writeheader()
		mic = 0
		for x in range(0,len(content)-1,2):		 
			for bit in content[x]:
				if bit == '1':
					mic = direction(int(content[x+1]))
				seconds = seconds + 0.02
				writer.writerow({'direction' : mic ,'seconds' : '{0:.2f}' .format(seconds),'speak': bit})

def direction(degree):
	if degree < 90:
		return 0
	elif degree < 180:
		return 1
	elif degree < 270:
		return 2
	elif degree < 360:
		return 3

def main():
	Transform()

if __name__ == '__main__':
	main()

