import pyaudio
import wave
from time import sleep

##########
# config #
##########
inputfile = "Traindata/mi/69.wav"

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100	# number of frames per second
CHUNK = 1024	# 
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "./file.wav"
TRAINDATAFILE = ["do/","re/","mi/","fa/","so/"]
PAUSEDATA = ["do_","re_","mi_","fa_","so_"]
PAUSEFILE = "pause/"


audio = pyaudio.PyAudio()
sleep(1)
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []
 
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
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

print("======= start  record =======")
frames = []
for j in range(0,int(RATE/CHUNK)):
	data = stream.read(CHUNK)
	frames.append(data)
waveFile = wave.open(inputfile, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
frames = frames[int(RATE/CHUNK//2):]
waveFile.writeframes(b''.join(frames[:]))
waveFile.close()
print("======= stop =======")


print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
