import csv
import wave
import numpy as np

def Transform(filenamein='output.txt', filenameout='output.csv', wavfile='output.wav'):
	with open(filenamein,'r') as f:
		content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	seconds = 0
	wave_data, time = WaveData(wavfile)
	print(len(wave_data))
	with open(filenameout, 'w') as f:
		fieldnames = ['direction','seconds','speak','amplitude']
		writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
		writer.writeheader()
		mic = 0
		for x in range(0,len(content)-2,2):		 
			for bit in content[x]:
				if bit == '1':
					mic = direction(int(content[x+1]))
				seconds = seconds + 0.02
				rang = np.where(((seconds-0.001) <= time) & (time <= (seconds+0.001)))
				suma = 0
				for y in rang[0]:
					suma += abs(wave_data[y])
		
				prom = '{0:.2f}' .format(suma/len(rang[0]))
				writer.writerow({'direction' : mic ,'seconds' : '{0:.2f}' .format(seconds),'speak': bit, 'amplitude': prom })

def direction(degree):
	if degree < 90:
		return 0
	elif degree < 180:
		return 1
	elif degree < 270:
		return 2
	elif degree < 360:
		return 3

def WaveData(wavfile):
	f = wave.open(wavfile, 'r')
	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_data = f.readframes(nframes)
	f.close()
	wave_data = np.fromstring(str_data, dtype=np.short)
	wave_data.shape = -1, 4
	wave_data = wave_data.T	
	#Tiempo asociado a un frame, un frame es una posicion en el arreglo
	time = np.arange(0, nframes) * (1.0 / framerate)
	print(len(time))
	return wave_data[0], time

def main():
	Transform()

if __name__ == '__main__':
	main()

