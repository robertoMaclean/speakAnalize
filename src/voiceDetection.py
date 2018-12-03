import sys
sys.path.append('/home/pi/audioProject/lib/')
import webrtcvad
import numpy as np
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from mic_array.pixels import pixels
from mic_array.mic_array import MicArray
import pyaudio
import mic_array.transform as transform
from public import *
import audioAnalize
import sys, os
from gpiozero import Button

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 30    # ms
TIME_VAD = float(float(VAD_FRAMES)/1000)
#DOA_FRAMES = 200    # ms
DOA_FRAMES =400   # ms
FILE_PATH = '/home/pi/audioProject/files/data/'
start_record = False
stop_record = False
btn = Button(12)
TXT_PATH = ''
CSV_PATH = ''
WAV_PATH = ''
def main():
	vad = webrtcvad.Vad(3)
	speech_count = 0
	chunks = []
	user = [[],[],[],[]]
	user.append([])
	user.append([])
	user.append([])
	user.append([])
	doa_chunks = int(DOA_FRAMES / VAD_FRAMES)
	current_time = time.strftime("%H-%M-%S")
	REL_PATH = '/speak_activity_'+current_time
	global CSV_PATH	
	global TXT_PATH	
	WAV_FILE = 'speak_activity_'+current_time+'.wav'
	TXT_PATH = FILE_PATH+time.strftime("%d-%m-%Y")+REL_PATH+'.txt'
	CSV_PATH = FILE_PATH+time.strftime("%d-%m-%Y")+REL_PATH+'.csv'    
	path = os.path.abspath(FILE_PATH)+'/'+time.strftime("%d-%m-%Y")+'/'
	EnsureDir(path)
	file = open(TXT_PATH,'w')
	frames = []
	try:			
		with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000, path+WAV_FILE)  as mic:
			newArrival = True
			tiempo = 0
			pixels.listen()
			firstime = True
			for chunk in mic.read_chunks():	
				if not btn.is_pressed:	
					stop_record = True
					file.close()
					global WAV_PATH
					WAV_PATH = path+WAV_FILE
					pixels.think()
					mic.stop()
					print "Stop Recording"
					return [TXT_PATH, WAV_PATH]		
				if(firstime):	
					global start_record			
					start_record = True
					firstime = False
				
				# Use single channel audio to detect voice activity
				if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
					speech_count += 1
					sys.stdout.write('1')
					file.write('1')                   
				else:
					sys.stdout.write('0') 
					file.write('0')

				tiempo = TIME_VAD + tiempo				
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
	except ValueError as value:
		print "excepcion", value
		return ['', '']
	
def wait_button():
	btn.wait_for_release()
	time.sleep(1)
	result = main()
	if(result[0]!= ''):
		transform.Transform(TXT_PATH, CSV_PATH, WAV_PATH, RATE, TIME_VAD)
		pixels.off()

def test():
	while True:
		btn.wait_for_release()
		if(btn.inactive_time>5):
			print("apagado")

	


if __name__ == '__main__':
# 	main()
#	wait_button()
	test()
