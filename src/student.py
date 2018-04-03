import matplotlib.pyplot as plt
import numpy as np
import scipy
import librosa
import librosa.display
from public import *
import public
import emotion
import csv
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import read
import soundfile as sf
import wave

class StudentAnalyze(object):


	# def play(self):
	# 	winsound.PlaySound(self.filename, winsound.SND_FILENAME)

	"""docstring for studentAnalyze"""
	def __init__(self, name):
		self.name = name
		self.filename = "../files/data/output.wav"
		self.intervention = []
		self.interventionTime = []
		self.interventionTotalTime = 0
		self.interventionSpeakTime = []
		self.interventionTotalSpeakTime = 0
		self.interventionCount = 0
		self.energyInterventionAVG = []
		self.energyInterventionTotalAVG = 0
		self.emotion = []
		self.interventionInit = []
		self.interventionEnd = []
		self.interventionSegmentCount = []


	def Analyze(self):
		#y, sr = librosa.load(self.filename)
		#oenv = librosa.onset.onset_strength(y=y, sr=sr)
		# Detect events without backtracking
		#onset_raw = librosa.onset.onset_detect(onset_envelope=oenv)
		# Backtrack the events using the onset envelope
		#onset_bt = librosa.onset.onset_backtrack(onset_raw, oenv)
		# Backtrack the events using the RMS energy
		#rmse = librosa.feature.rmse(S=np.abs(librosa.stft(y=y)))
		#onset_bt_rmse = librosa.onset.onset_backtrack(onset_raw, rmse[0])
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

		#self.Intervention(onset_bt)
		print self.filename
		f = wave.open(self.filename, 'rb')
		params = f.getparams()
		nchannels, sampwidth, framerate, nframes = params[:4]
		print "channels", nchannels
		str_data = f.readframes(nframes)
		f.close()

		wave_data = np.fromstring(str_data, dtype=np.short)
		wave_data.shape = -1, 4
		wave_data = wave_data.T
		time = np.arange(0, nframes) * (1.0 / framerate)
		figure = plt.gcf() # get current figure
		figure.set_size_inches(8*20, 6)
		duration = nframes/float(framerate)
		xticks = np.arange(0, duration, 2)
		plt.subplot(211).set_xticks(xticks)
		plt.plot(time, wave_data[0])
		plt.xlabel("time (seconds)")
		plt.vlines(activity[0], 0, wave_data[0].max(), label='Usuario 1', color='red')
		plt.vlines(activity[1], 0, wave_data[0].max(), label='Usuario 2', color='blue')
		plt.vlines(activity[2], 0, wave_data[0].max(), label='Usuario 3', color='green')
		plt.vlines(activity[3], 0, wave_data[0].max(), label='Usuario 4', color='orange')
		plt.legend(frameon=True, framealpha=0.6)
		# plt.subplot(412).set_xticks(xticks)
		# plt.plot(time, wave_data[1], c="g")
		# plt.xlabel("time (seconds)")
		# plt.title('channel 2', loc='left')

		# plt.subplot(413).set_xticks(xticks)
		# plt.plot(time, wave_data[2], c="g")
		# plt.xlabel("time (seconds)")
		# plt.title('channel 3', loc='left')

		# plt.subplot(414).set_xticks(xticks)
		# plt.plot(time, wave_data[3], c="g")
		# plt.xlabel("time (seconds)")
		# plt.title('channel 4', loc='left')

		plt.show()
		#plt.show()
		plt.close(figure)
		#self.plot(audio) 
		#intervention = librosa.time_to_frames(self.intervention)[0]
		#self.InterventionTotalTime()
		#self.InterventionTotalSpeakTime()
		#self.InterventionCount()
		#self.EnergyInterventionTotalAVG(oenv, onset_raw)
		#print("int time: ",self.intervention)
		#vlines = []
		#vlines.append(onset_raw[0::len(onset_raw)-1])
		#self.Plot(values=oenv, valueLabel="Intensidad voz", xlabel="Frames", ylabel="Intensidad", vlines=[librosa.time_to_frames(self.interventionInit),librosa.time_to_frames(self.interventionEnd)], vlinesLabels=["Inicio Interv.","Fin Interv."],color=["green","red"])
		#self.Plot(values=oenv, valueLabel="valueLabel", xlabel="hola", ylabel="chao", hlines=[[self.energyInterventionTotalAVG]],hlinesLabels=["asd"])
		#(self, values, valueLabel, xlabel, ylabel, vlines=[], vlinesLabels=[])
		# self.Emotion()

	def Segment(self, segmentList):
		initpos = 0
		initialTimeSegment = []
		finalTimeSegment = []
		frames = librosa.time_to_frames(1)
		for x in range(0,len(segmentList)-1):
			#print("habla: ",librosa.frames_to_time(x, sr=sr))
			if((segmentList[x+1]-segmentList[x])>frames):
				initialTimeSegment.append(float("{0:.2f}".format(segmentList[initpos])))
				finalTimeSegment.append(float("{0:.2f}".format(segmentList[x]))) 
				initpos = x+1
			elif(x+1 == len(segmentList)-1):
				initialTimeSegment.append(float("{0:.2f}".format(segmentList[initpos])))
				finalTimeSegment.append(float("{0:.2f}".format(segmentList[x+1])))

		initialTimeSegment = librosa.frames_to_time(initialTimeSegment)
		finalTimeSegment = librosa.frames_to_time(finalTimeSegment)
		#2 decimal format
		for x in range(0,len(initialTimeSegment)):
			initialTimeSegment[x]= float("{0:.2f}".format(initialTimeSegment[x]))
			finalTimeSegment[x]= float("{0:.2f}".format(finalTimeSegment[x]))
		self.interventionSegmentCount.append(len(initialTimeSegment))
		return [initialTimeSegment, finalTimeSegment]
	
	def Intervention(self, interList):
		initpos = 0
		#Segundos a frames
		frames = librosa.time_to_frames(4)[0]	
		for x in range(0,len(interList)-1):
			if((interList[x+1]-interList[x])>frames):	
				print("interList: ",interList)
				self.intervention.append(self.Segment(interList[initpos:x]))
				initpos = x+1
			elif((x+1) == (len(interList)-1)):
				self.intervention.append(self.Segment(interList[initpos:x+2]))

		#print(self.InterventionTotalTime(self.intervention))
		#print(self.TotalInterventionSpeakTime(self.intervention))

	def InterventionTime(self, interList):
		self.interventionTime.append(float("{0:.2f}".format(interList[1][-1]-interList[0][0])))
		self.interventionInit.append(interList[0][0])
		self.interventionEnd.append(interList[1][-1])

	def  InterventionTotalTime(self):
		for x in range(0, len(self.intervention)):
			self.InterventionTime(self.intervention[x])
		self.interventionTotalTime = sum(self.interventionTime)

	def InterventionSpeakTime(self, interList):
		total = 0
		for x in range(0,len(interList[0])):
			total += interList[1][x]-interList[0][x]
		self.interventionSpeakTime.append(float("{0:.2f}".format(total)))

	def InterventionTotalSpeakTime(self):
		for x in range(0, len(self.intervention)):
			self.InterventionSpeakTime(self.intervention[x])
		self.interventionTotalSpeakTime = sum(self.interventionSpeakTime)
		

	def InterventionCount(self):
		self.interventionCount = len(self.intervention)

	def EnergyInterventionAVG(self, oenv, onset_raw, init, end):
		total = 0
		count = 0
		# start = intervention[0][0]
		# end = intervention[1][-1]
		# start = onset_bt.tolist().index(start)
		# end = onset_bt.tolist().index(end)+1
		for x in onset_raw:
			if((x>init) and (x<end)):
				total += oenv[x]
				count += 1
		self.energyInterventionAVG.append(float("{0:.2f}".format(total/count)))
		

	def EnergyInterventionTotalAVG(self, oenv, onset_raw):
		for x in range(0, len(self.interventionInit)):
			self.EnergyInterventionAVG(oenv, onset_raw, librosa.time_to_frames(self.interventionInit[x]),librosa.time_to_frames(self.interventionEnd[x]))
		self.energyInterventionTotalAVG = sum(self.energyInterventionAVG)/len(self.energyInterventionAVG)
		 
	def Emotion(self):
		labels = ["neutral", "feliz", "triste", "enojo", "miedo"]
		self.emotion = emotion.Emotion("../files/audio.wav")
		self.emotion = self.emotion.EmotionAnalyze()
		self.CakePlot(labels, self.emotion)

	def CakePlot(self, labels, values):
		filepath = "../files/student/"+self.name+"/"
		fig1, ax1 = plt.subplots(figsize=(5,4))

		ax1.pie(values , labels=labels, autopct='%1.1f%%', shadow=True, startangle=0)
		ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
		EnsureDir(filepath=filepath)
		plt.savefig(filepath+"Emotion")
		plt.show()

	def plot(self, y):
		# Detect onset force
		#oenv = librosa.onset.onset_strength(y=y, sr=sr)
		# Detect events without backtracking
		#onset_raw = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=False)
		# Backtrack the events using the onset envelope
		#onset_bt = librosa.onset.onset_backtrack(onset_raw, oenv)
		# Backtrack the events using the RMS energy
		#rmse = librosa.feature.rmse(S=np.abs(librosa.stft(y=y)))
		#onset_bt_rmse = librosa.onset.onset_backtrack(onset_raw, rmse[0])
		# print("oenv", oenv)
		# print("onset_raw", onset_raw)
		# print("onset_bt", onset_bt)
		# print("rmse",rmse)
		# print("onset_bt_rmse", onset_bt_rmse)
		# onset_bt_rmse_tiempo = librosa.frames_to_time(onset_bt_rmse, sr=sr)
		# print("actividad en el tiempo: ", onset_bt_rmse)
		plt.figure()

		#plt.subplot(2,1,1)
		plt.plot(y, label='Onset strength')
		#plt.vlines(onset_raw, 0, oenv.max(), label='Raw onsets')
		#plt.vlines(onset_bt, 0, oenv.max(), label='Backtracked', color='r')
		plt.legend(frameon=True, framealpha=0.75)
		plt.ylabel("amplitud")
		plt.xlabel("frames")
		# plt.subplot(2,1,2)
		# plt.plot(rmse[0], label='RMSE')
		# plt.vlines(onset_bt_rmse, 0, rmse.max(), label='Backtracked (RMSE)', color='r')
		# plt.legend(frameon=True, framealpha=0.75)
		# plt.ylabel("amplitud")
		# plt.xlabel("frames")
		plt.show()	

	def Plot(self, values, valueLabel="", xlabel="", ylabel="", vlines=[], hlines=[], vlinesLabels=[], hlinesLabels=[], color=[]):
		plt.figure(figsize=(4, 4))
		plt.plot(values, label=valueLabel)
		if(len(vlines)==len(vlinesLabels)):
			for x in range(0, len(vlines)):
				plt.vlines(vlines[x], 0, values.max(), label=vlinesLabels[x], color=color[x])
		if(len(hlines)==len(hlinesLabels)):
			for x in range(0, len(hlines)):
				plt.hlines(hlines[x], 0, len(values), label=hlinesLabels[x])
		plt.legend(frameon=True, framealpha=0.75)
		plt.ylabel(ylabel)
		plt.xlabel(xlabel)
		filepath = "../files/student/"+self.name+"/"
		EnsureDir(filepath)
		plt.savefig(filepath+"strength")
	
if __name__ == '__main__':
 	studentList = []
	studentAnalyze = StudentAnalyze
	student = studentAnalyze("pedro")
	#student2 = studentAnalyze("juan")
	student.Analyze()
	#student2.Analyze()
	studentList.append(student)
	#studentList.append(student2)
	# print("variables individuales")
	# print("nombre estudiante: ", student.name)
	# #print("intervenciones: ", student.intervention)
	# print("tiempo intervenciones: ", student.interventionTime)
	# print("tiempo total intervenciones: ", student.interventionTotalTime)
	# print("tiempo de habla por intervenciones: ", student.interventionSpeakTime)
	# print("tiempo de total de habla: ", student.interventionTotalSpeakTime)
	# print("cantidad de intervenciones: ", student.interventionCount)
	# print("enegia promedio voz por intervenciones: ", student.energyInterventionAVG)
	# print("energia promedio total: ", student.energyInterventionTotalAVG)