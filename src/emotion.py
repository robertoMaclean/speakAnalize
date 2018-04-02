import sys
import scipy.io.wavfile

sys.path.append("../lib/api")
import Vokaturi

class Emotion(object):
	"""docstring for Emotion"""
	def __init__(self, filepath):
		self.filepath = filepath

	def EmotionAnalyze(self):	
		print ("Loading library...")
		Vokaturi.load("../lib/lib/Vokaturi_win32.dll")
		print ("Analyzed by: %s" % Vokaturi.versionAndLicense())

		print ("Reading sound file...")
		file_name = "../files/audio.wav"
		print("filename: ",self.filepath)
		(sample_rate, samples) = scipy.io.wavfile.read(self.filepath)
		print ("   sample rate %.3f Hz" % sample_rate)

		print ("Allocating Vokaturi sample array...")
		buffer_length = len(samples)
		print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
		c_buffer = Vokaturi.SampleArrayC(buffer_length)
		if samples.ndim == 1:  # mono
			c_buffer[:] = samples[:] / 32768.0
		else:  # stereo
			c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

		print ("Creating VokaturiVoice...")
		voice = Vokaturi.Voice (sample_rate, buffer_length)

		print ("Filling VokaturiVoice with samples...")
		voice.fill(buffer_length, c_buffer)

		print ("Extracting emotions from VokaturiVoice...")
		quality = Vokaturi.Quality()
		emotionProbabilities = Vokaturi.EmotionProbabilities()
		voice.extract(quality, emotionProbabilities)
		response = []
		if quality.valid:
			response.append(emotionProbabilities.neutrality)
			response.append(emotionProbabilities.happiness)
			response.append(emotionProbabilities.sadness)
			response.append(emotionProbabilities.anger)
			response.append(emotionProbabilities.fear)
		else:
			print ("Not enough sonorancy to determine emotions")
			return none

		voice.destroy()
		return response
