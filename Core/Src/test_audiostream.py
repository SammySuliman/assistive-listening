import sounddevice as sd
import numpy as np

SAMPLERATE = 16000  # Hz, typical mic sample rate
BLOCKSIZE = 1024    # samples per block
CHANNELS = 1        # mono

print("Recording from your PC microphone. Speak into it...")

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    # Play input directly to output (monitor your voice)
    outdata[:] = indata

# Open input + output stream
with sd.Stream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE,
               channels=CHANNELS, dtype='float32', callback=callback):
    print("Press Ctrl+C to stop.")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopped.")