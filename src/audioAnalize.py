import csv
import wave
import numpy as np
#import matplotlib.pyplot as plt

filename = "../files/data/output.wav"

def Analize():
	isSpeak = False
	activity = []
	activity.append([])
	activity.append([])
	activity.append([])
	activity.append([])

	with open('../files/data/output.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=";")
		for row in reader:
			if int(row['speak']):
				isSpeak = True
				activity[int(row['direction'])].append(float(row['seconds'])) 
			#else:
	f = wave.open(filename, 'rb')
	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_data = f.readframes(nframes)
	f.close()

	wave_data = np.fromstring(str_data, dtype=np.short)
	wave_data.shape = -1, 4
	wave_data = wave_data.T
	time = np.arange(0, nframes) * (1.0 / framerate)
	# figure = plt.gcf() # get current figure
	# figure.set_size_inches(8*20, 6)
	# duration = nframes/float(framerate)
	# xticks = np.arange(0, duration, 2)
	print np.mean(wave_data, axis = 1)
	# plt.subplot(211).set_xticks(xticks)
	# plt.plot(time, wave_data[0])
	# plt.xlabel("time (seconds)")
	# plt.vlines(activity[0], 0, wave_data[0].max(), label='Usuario 1', color='red')
	# plt.vlines(activity[1], 0, wave_data[0].max(), label='Usuario 2', color='blue')
	# plt.vlines(activity[2], 0, wave_data[0].max(), label='Usuario 3', color='green')
	# plt.vlines(activity[3], 0, wave_data[0].max(), label='Usuario 4', color='orange')
	# plt.legend(frameon=True, framealpha=0.6)
	# plt.show()
	# plt.close(figure)

if __name__ == '__main__':
	Analize()