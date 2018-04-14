import csv
import wave
import numpy as np
import matplotlib.pyplot as plt

filename = "../files/data/output.wav"

def Analize():
	activity = [[],[],[],[]]
	interTimes = [[],[],[],[]]
	timeActivity = []
	lastPosition = -1	
	with open('../files/data/output.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=";")
		for row in reader:
			if int(row['speak']):
				if int(row['direction']) != lastPosition:
					if lastPosition != -1:
						interTimes[lastPosition].append(timeActivity)
						timeActivity = []
				
				timeActivity.append(float(row['seconds']))
				lastPosition = int(row['direction'])
				activity[lastPosition].append(float(row['seconds']))
		print 'intervenciones Usuario 1\n', interTimes[0]
		print 'intervenciones Usuario 2\n', interTimes[1]
		print 'intervenciones Usuario 3\n', interTimes[2]
		print 'intervenciones Usuario 4\n', interTimes[3]
	f = wave.open(filename, 'rb')
	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_data = f.readframes(nframes)
	f.close()

	wave_data = np.fromstring(str_data, dtype=np.short)
	wave_data.shape = -1, 4
	wave_data = wave_data.T
	time = np.arange(0, nframes) * (1.0 / framerate)
	#print '{0:.2f}'.format(interTimes[0][0][0])
	#print np.where(time == '{0:.2f}'.format(interTimes[0][0][0]))
	figure = plt.gcf() # get current figure
	figure.set_size_inches(8*20, 6)
	duration = nframes/float(framerate)
	xticks = np.arange(0, duration, 2)
	#print np.mean(wave_data, axis = 1)
	plt.subplot(411).set_xticks(xticks)
	plt.plot(time, abs(wave_data[0]))
	plt.subplot(412).set_xticks(xticks)
	plt.plot(time, abs(wave_data[1]))
	plt.subplot(413).set_xticks(xticks)
	plt.plot(time, abs(wave_data[2]))
	plt.subplot(414).set_xticks(xticks)
	plt.plot(time, abs(wave_data[3]))
	plt.xlabel("time (seconds)")
	# plt.vlines(activity[0], 0, wave_data[0].max(), label='Usuario 1', color='red')
	# plt.vlines(activity[1], 0, wave_data[0].max(), label='Usuario 2', color='blue')
	# plt.vlines(activity[2], 0, wave_data[0].max(), label='Usuario 3', color='green')
	# plt.vlines(activity[3], 0, wave_data[0].max(), label='Usuario 4', color='orange')
	plt.legend(frameon=True, framealpha=0.6)
	plt.show()
	plt.close(figure)

if __name__ == '__main__':
	Analize()