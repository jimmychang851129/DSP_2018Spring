import pyaudio
import wave
from time import sleep
import numpy
##########
# config #
##########
st = 76

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100	# number of frames per second
CHUNK = 1024	# 
RECORD_SECONDS = 25
WAVE_OUTPUT_FILENAME = "./file.wav"
TRAINDATAFILE = ["Traindata/do/","Traindata/re/","Traindata/mi/","Traindata/fa/","Traindata/so/"]
PAUSEDATA = ["do_","re_","mi_","fa_","so_"]
PAUSEFILE = "Traindata/pause/"

print("recording...")
frames = []

# start Recording
pause_cnt = 0
print("======= Instruction =======")
print("======= 吹一個音階(do~so)，反覆吹 =======")
print("======= 一個start吹一個音，stop時停止吹，直到出現下一個start =======")
print("======= 所以一個出現五個start照理來講要吹完一次do~so =======")
print("")
print("")
print("")
print("")
print("")
sleep(1)
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK) 
for i in range(RECORD_SECONDS):
	print("======= start  record",TRAINDATAFILE[i%5],int(st+i//5),"=======")
	frames = []
	for j in range(0,int(RATE/CHUNK)):
		data = stream.read(CHUNK)
		frames.append(data)
	waveFile = wave.open(TRAINDATAFILE[i%5]+"%02d"%(st+i/5)+".wav", 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	frames = frames[int(RATE/CHUNK//5):]
	waveFile.writeframes(b''.join(frames))
	waveFile.close()
	print("======= stop =======")
	pause = []
	for j in range(0,int(RATE/CHUNK)):
		data = stream.read(CHUNK)
		pause.append(data)
	# waveFile = wave.open(PAUSEFILE+PAUSEDATA[i%5]+"%02d"%(st+i/5)+".wav", 'wb')
	# waveFile.setnchannels(CHANNELS)
	# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	# waveFile.setframerate(RATE)
	# pause = pause[int(RATE/CHUNK//2):]
	# waveFile.writeframes(b''.join(pause))
	# waveFile.close()
	# pause_cnt += 1


print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

#############
# Reference #
#############
# https://stackoverflow.com/questions/39474111/recording-audio-for-specific-amount-of-time-with-pyaudio

