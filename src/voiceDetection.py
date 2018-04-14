

import sys
sys.path.append('../lib/')
import webrtcvad
import numpy as np
import time
from mic_array.mic_array import MicArray
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from mic_array.pixels import pixels
import pyaudio
import mic_array.transform as transform

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 20     # ms
#DOA_FRAMES = 200    # ms
DOA_FRAMES =300   # ms
FILE_NAME = '../files/data/output'
FILE_NAME_CSV = '../files/data/output'

def main():
	vad = webrtcvad.Vad(3)
	speech_count = 0
	chunks = []
	user = []
	user.append([])
	user.append([])
	user.append([])
	user.append([])
	doa_chunks = int(DOA_FRAMES / VAD_FRAMES)
	current_time = time.strtime("%x")+time.strtime("%X")
	FILE_NAME = FILE_NAME + current_time + '.txt'
	FILE_NAME_CSV = FILE_NAME_CSV + current_time + '.csv'    
	file = open(FILE_NAME,'w')
	frames = []
	try:	
			
		with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
			newArrival = True
			tiempo = 0
			pixels.listen()
			for chunk in mic.read_chunks():				
				# Use single channel audio to detect voice activity
				if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
					speech_count += 1
					sys.stdout.write('1')
					file.write('1')                   
				else:
					sys.stdout.write('0') 
					file.write('0')

				tiempo = 0.02 + tiempo				
				sys.stdout.flush()
				chunks.append(chunk)

				if len(chunks) == doa_chunks:					
					if speech_count > (doa_chunks / 2):
						frames = np.concatenate(chunks)
						direction = mic.get_direction(frames)
						print('\nTiempo: {0:.2f}' .format(tiempo))
						print('Direccion: {}'.format(int(direction)))
						pixels.wakeup(direction)
						if int(direction) < 90:
							micPos = 0
						elif int(direction) < 180:
							micPos = 1
						elif int(direction) < 270:
							micPos = 2
						else:
							micPos = 3

						user[micPos].append(float("{0:.2f}".format(tiempo)))
						file.write('\n{}' .format(int(direction)))
						file.write('\n')
						
					speech_count = 0
					chunks = []			
			time.sleep(1)
			mic.stop()
	except KeyboardInterrupt:
		pass
		file.close()
		print 'intervenciones' 		
		for x in range(0,len(user)):
			print "usuario", x+1,":", user[x] 
		print 'creando archivo: '+FILE_NAME
		transform.Transform(FILE_NAME, FILE_NAME_CSV)

if __name__ == '__main__':
	main()
