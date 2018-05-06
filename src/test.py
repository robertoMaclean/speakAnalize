import unittest, voiceDetection, time, os

class Test(unittest.TestCase):
	def setUp(self):
		data = voiceDetection.main()
		self.record_on = data[0]
		self.record_off = data[1]
		self.txt_file = data[2]
		self.csv_file = data[3]
		self.wav_file = data[4]

	def test_record_on(self):
	 	self.assertEqual(self.record_on, True)
		
	def test_record_off(self):
		self.assertEqual(self.record_off, True)

	def test_txt(self):
		is_file = os.path.isfile(self.txt_file)
		self.assertEqual(is_file, True)

	def test_csv(self):
		is_file = os.path.isfile(self.csv_file)
		self.assertEqual(is_file, True)

	def test_wav(self):
		is_file = os.path.isfile(self.wav_file)
		self.assertEqual(is_file, True)


		
		
		

		

if __name__ == '__main__':
	unittest.main()