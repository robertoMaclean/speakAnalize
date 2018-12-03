import unittest, voiceDetection, time, os, sys
sys.path.append('../lib/')
import mic_array.transform as transform
from mic_array.mic_array import MicArray
import threading, signal

class Test(unittest.TestCase):

	def record_on(self):
		try:			
			with MicArray(16000, 4) as mic:
				for chunk in mic.read_chunks():
					mic.stop()
					return True	
		except:
			return False

	def record_off(self):
		is_quit = threading.Event()

		def signal_handler(sig, num):
			is_quit.set()

		signal.signal(signal.SIGINT, signal_handler)
		try:			
			with MicArray(16000, 4) as mic:
				for chunk in mic.read_chunks():
					if is_quit.is_set():
						mic.stop()
						return True
		except:
			return False

	def test_record_on(self):
		start = self.record_on()
		if(start):
			print "El dispositivo ha iniciado correctamente"
	 	self.assertEqual(start, True)
		
	def test_record_off(self):
		stop = self.record_off()
		if(stop):
			print "\nEl dispositivo se ha detenido correctamente"
		self.assertEqual(stop, True)

	def test_txt(self):
		txt_file_path = voiceDetection.main()[0]
		print "\ngenerando archivo txt..."
		is_file = os.path.isfile(txt_file_path)
		print "existe el archivo?", is_file
		self.assertEqual(is_file, True)

	def test_wav(self):
		wav_file_path = voiceDetection.main()[1]
		print "\ngenerando archivo wav..."
		is_file = os.path.isfile(wav_file_path)
		print "existe el archivo?", is_file
		self.assertEqual(is_file, True)

	def test_csv(self):
		file_txt = "../files/test/file.txt"
		file_wav = "../files/test/file.wav"
		file_csv_output = "../files/test/file.csv"
		is_file = os.path.isfile(file_csv_output)
		print "antes de generar csv"
		print "existe el archivo?",is_file
		print "generando csv..."
		transform.Transform(filenamein=file_txt, wavfile=file_wav, filenameout=file_csv_output)
		is_file = os.path.isfile(file_csv_output)
		print "existe el archivo?",is_file
		self.assertEqual(is_file, True)
		print "borrando archivo..."
		os.remove(file_csv_output)
	

if __name__ == '__main__':
	unittest.main()