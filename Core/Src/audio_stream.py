import serial
import serial.tools.list_ports
import numpy as np
import sounddevice as sd

# -----------------------------
# 1️⃣ Find STM32 COM port automatically
# -----------------------------
def find_stm32_port():
    for port in serial.tools.list_ports.comports():
        if "STM32" in port.description or "USB Serial" in port.description:
            return port.device
    # fallback: pick the first available serial port
    return serial.tools.list_ports.comports()[0].device

COM_PORT = find_stm32_port()
BAUDRATE = 921600       # Must match STM32 UART
SAMPLE_WIDTH = 2        # bytes per sample (int16)
CHANNELS = 1            # mono audio

# -----------------------------
# 2️⃣ Open serial port
# -----------------------------
ser = serial.Serial(COM_PORT, BAUDRATE, timeout=1)

# -----------------------------
# 3️⃣ Audio parameters
# -----------------------------
SAMPLERATE = 3200       # Hz, calculated from DFSDM settings
BLOCKSIZE = 512         # number of samples per audio block

# -----------------------------
# 4️⃣ Continuous streaming
# -----------------------------
print(f"Streaming audio from {COM_PORT} at {SAMPLERATE} Hz...")
with sd.OutputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16') as stream:
    while True:
        # read BLOCKSIZE samples
        data = ser.read(BLOCKSIZE * SAMPLE_WIDTH)
        if len(data) < BLOCKSIZE * SAMPLE_WIDTH:
            continue  # incomplete block
        samples = np.frombuffer(data, dtype=np.int16)

        # optional: normalize to float32 [-1, 1]
        samples = samples.astype(np.float32) / 32768.0

        # play audio
        stream.write(samples)