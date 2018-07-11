import csv
import wave
import numpy as np
import time as tiempo

def Transform(filenamein='../../files/data/output.txt', filenameout='../../files/data/output.csv', wavfile='../../files/data/output.wav', RATE = 16000):
	with open(filenamein,'r') as f:
		content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	seconds = 0
	wave_data, time = WaveData(wavfile)
	with open(filenameout, 'w') as f:
		fieldnames = ['direction','seconds','speak','amplitude']
		writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
		writer.writeheader()
		mic = 0
		pos = 0
		for x in range(0,len(content)-2,2):		 
			for bit in content[x]:
				seconds = seconds + 0.02
				if bit == '1':
					mic = direction(int(content[x+1]))
					#print(len(time)/16000)
					seconds_left = int((seconds-0.0001)*RATE)
					seconds_right = int((seconds+0.0001)*RATE) 
					short_time = time[seconds_left:seconds_right]
					#print(time[seconds_left:seconds_right])
					#rang = np.where((seconds-0.0001 <= short_time) & (short_time <= seconds+0.0001))
					#print('rang',rang[0])
					#print('len',len(rang[0]))
					suma = 0
					div = 0
					for y in range(seconds_left,seconds_right):
					 	suma += abs(wave_data[y])
					 	div += 1
				else:
				 	div = 1
					suma = 0	
				prom = '{0:.2f}' .format(suma/div)
				#print('prom', prom)
				writer.writerow({'direction' : mic ,'seconds' : '{0:.2f}' .format(seconds),'speak': bit, 'amplitude': prom })
				pos += 1
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
	return wave_data[0], time

def main():
	Transform()

if __name__ == '__main__':
	main()

