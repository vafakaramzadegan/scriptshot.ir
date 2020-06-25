# Tutorial Video available on: https://www.aparat.com/v/wOxQg

from pyaudio import PyAudio
import struct
import math

wav = open("music.wav", "rb", 0)

wav.seek(22)

numChannels = struct.unpack('<h', wav.read(2))[0]
print("numChannels: ", numChannels)
sampleRate = math.floor(struct.unpack('<l', wav.read(4))[0] * 0.9)
print("sampleRate: ", sampleRate)

wav.seek(34)

bitsPerSample = struct.unpack('<h', wav.read(2))[0]
print("bitsPerSample: ", bitsPerSample)

p = PyAudio()

stream = p.open(format = p.get_format_from_width(bitsPerSample / 8),
                channels = numChannels,
                rate = sampleRate,
                output = True)

data = wav.read(sampleRate)
while data:
    stream.write(data)
    data = wav.read(sampleRate)
    
stream.stop_stream()
stream.close()
p.terminate()

wav.close
