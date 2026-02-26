import serial
import serial.tools.list_ports
import numpy as np
import wave
import time

def find_stm32_port():
    for port in serial.tools.list_ports.comports():
        if "STM32" in port.description or "USB Serial" in port.description:
            return port.device
    # fallback: pick the first available serial port
    return serial.tools.list_ports.comports()[0].device

# Serial port settings — update to your STM32 COM port and baud rate
SERIAL_PORT = find_stm32_port()
BAUD_RATE = 921600

SAMPLES_PER_FRAME = 1024
BYTES_PER_SAMPLE = 2
FRAME_SIZE = SAMPLES_PER_FRAME * BYTES_PER_SAMPLE

OUTPUT_WAV_FILE = "received_audio.wav"
SAMPLE_RATE = 16000

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.0)
    print(f"Opened serial port {SERIAL_PORT} at {BAUD_RATE} baud")

    audio_data = []

    try:
        start_time = time.time()
        print("Receiving audio... Press Ctrl+C to stop and save")

        while True:
            print("hello hello")
            data = ser.read(FRAME_SIZE)  # read up to 1024 samples (2048 bytes)
            if data:
                print("goodbye goodbye")
                if len(data) % 2 != 0:
                    # Make sure we have even number of bytes for int16 conversion
                    data = data[:-1]
                print(f"Received {len(data)} bytes")
                samples = np.frombuffer(data, dtype=np.int16)
                audio_data.append(samples)

    except KeyboardInterrupt:
        print("\nStopping reception and saving WAV file...")

    ser.close()

    if len(audio_data) == 0:
        print("No audio data received.")
        return

    # Concatenate all received samples into one array
    all_samples = np.concatenate(audio_data)

    # Save to WAV file
    with wave.open(OUTPUT_WAV_FILE, 'wb') as wf:
        wf.setnchannels(1)          # Mono audio
        wf.setsampwidth(2)          # 16-bit samples
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(all_samples.tobytes())

    print(f"Saved {len(all_samples)} samples to {OUTPUT_WAV_FILE}")

if __name__ == "__main__":
    main()