
import pyaudio

_pa = pyaudio.PyAudio()

print(_pa.get_sample_size(pyaudio.paInt16))