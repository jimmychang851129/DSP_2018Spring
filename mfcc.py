import numpy 
import scipy.io.wavfile
from scipy.fftpack import dct

##########
# config #
##########
frame_size = 0.025		# 一個frame 大小(25MS)
frame_stride = 0.01		# frame移動要overlap
NFFT = 512
nfilt = 40
num_ceps = 12			#取前12維
cep_lifter = 22
DATA_NUM = 81
SIGNAL_SIZE = 35840

def refine(signal):
	sum = abs(numpy.sum(signal,axis=1))
	ind = numpy.argsort(sum)
	mean = numpy.mean(ind[-1000:])
	# print("mean = ",mean,signal[int(mean)])
	if mean + 5000 >= SIGNAL_SIZE:
		mean = SIGNAL_SIZE - 5000
	elif mean - 5000 < 0:
		mean  = 5000
	return signal[int(mean)-5000:int(mean)+5000]


########
# data #
########
music = ["do/","re/","mi/","fa/","so/"]
###################
#	Read wav data #
###################
for t in music:
	alldata = []
	for i in range(DATA_NUM):
		sample_rate, signal = scipy.io.wavfile.read("Traindata/"+t+"%02d"%(i)+".wav")
		signal = refine(signal)
		# print("signal shape = ",signal.shape) # (35840,2)
		#################
		# pre-emphasize #
		#################
		pre_emphasis = 0.97
		emphasized_signal = numpy.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

		###########
		# framing #
		###########
		frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
		signal_length = len(emphasized_signal)
		frame_length = int(round(frame_length))
		frame_step = int(round(frame_step))
		num_frames = int(numpy.ceil(float(numpy.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame

		pad_signal_length = num_frames * frame_step + frame_length
		z = numpy.zeros((pad_signal_length - signal_length))
		pad_signal = numpy.append(emphasized_signal, z) # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal

		indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) + numpy.tile(numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
		frames = pad_signal[indices.astype(numpy.int32, copy=False)]

		##################
		# hamming window #
		##################
		frames *= numpy.hamming(frame_length)

		#######
		# FFT #
		#######
		mag_frames = numpy.absolute(numpy.fft.rfft(frames, NFFT))
		pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))

		#####################
		# triangular filter #
		#####################
		low_freq_mel = 0
		high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
		mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
		hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
		bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)

		fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
		for m in range(1, nfilt + 1):
		    f_m_minus = int(bin[m - 1])   # left
		    f_m = int(bin[m])             # center
		    f_m_plus = int(bin[m + 1])    # right
		    for k in range(f_m_minus, f_m):
		        fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
		    for k in range(f_m, f_m_plus):
		        fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])

		filter_banks = numpy.dot(pow_frames, fbank.T)
		filter_banks = numpy.where(filter_banks == 0, numpy.finfo(float).eps, filter_banks)  # Numerical Stability
		filter_banks = 20 * numpy.log10(filter_banks)  # dB
		##############################
		# discrete consine transform #
		##############################
		#############
		# Normalize #
		#############
		filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
		
		mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : (num_ceps + 1)] # Keep 2-13
		(nframes, ncoeff) = mfcc.shape
		n = numpy.arange(ncoeff)
		lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
		mfcc *= lift
		# print("mfcc size = ",mfcc.shape)
		#############
		# Normalize #
		#############
		# filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
		mfcc -= (numpy.mean(mfcc, axis=0) + 1e-8)
		a = []
		for i in range(mfcc.shape[0]):
			a.append([])
			first = numpy.gradient(mfcc[i],1)
			second = numpy.gradient(mfcc[i],2)
			tmp = mfcc[i]
			tmp = numpy.append(tmp,first)
			tmp = numpy.append(tmp,second)
			a[i] = tmp
		alldata.append(numpy.array(a))		# not sure should get mfcc or filter banks
		# alldata.append(mfcc)
	alldata = numpy.array(alldata)
	print("alldata shape = ",alldata.shape)
	numpy.save("MFCC/"+t+"test",alldata)
#############
# Reference #
#############
# http://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html