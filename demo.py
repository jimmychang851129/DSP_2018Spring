import pyaudio
import wave
import os
import time
import sys
import numpy as np
import train

from threading import Timer,Thread,Event


class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      time.sleep(0.2)
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    print("# ")

t = perpetualTimer(1,printer)


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100	# number of frames per second
CHUNK = 1024	# 
RECORD_SECONDS = 9
WAVE_OUTPUT_FILENAME = "./doremi.wav"

###########
# setting #
###########
###########
# prepare #
###########
for i in range(3,0,-1):
	print(i,"... ",end='')
	sys.stdout.flush()
	time.sleep(1)
print("start !!!!")
# t.start()
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
frames = []
for i in range(RECORD_SECONDS):
  print("======= start  record second",i,"=======")
  for j in range(0,int(RATE/CHUNK)):
    data = stream.read(CHUNK)
    frames.append(data)
  print("===== stop =====")
  pause = []
  for j in range(0,int(RATE/CHUNK)):
    data = stream.read(CHUNK)
    pause.append(data)

# t.cancel()
waveFile = wave.open("Testdata/doremi.wav", 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
print("finish recording ...")
#############
# Refernece #
#############
# https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds