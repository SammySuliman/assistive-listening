import serial
import serial.tools.list_ports
import numpy as np
import wave

def find_stm32_port():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        if "STM32" in port.description or "USB Serial" in port.description:
            return port.device

    if len(ports) == 0:
        raise RuntimeError("No serial ports found")

    return ports[0].device

SERIAL_PORT = find_stm32_port()
BAUD_RATE = 921600

CHANNELS = 1
SAMPLES_PER_FRAME = 512
BYTES_PER_SAMPLE = 2
FRAME_SIZE = SAMPLES_PER_FRAME * BYTES_PER_SAMPLE

OUTPUT_WAV_FILE = "received_audio_w_beamforming.wav"
SAMPLE_RATE = 16000

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.0)
    print(f"Opened serial port {SERIAL_PORT} at {BAUD_RATE} baud")

    audio_data = []

    try:
        print("Receiving mono beamformed audio... Press Ctrl+C to stop and save")

        while True:
            data = ser.read(FRAME_SIZE)

            if len(data) != FRAME_SIZE:
                continue

            samples = np.frombuffer(data, dtype=np.int16)
            audio_data.append(samples.copy())

    except KeyboardInterrupt:
        print("\nStopping reception and saving WAV file...")

    ser.close()

    if len(audio_data) == 0:
        print("No audio data received.")
        return

    all_samples = np.concatenate(audio_data)

    with wave.open(OUTPUT_WAV_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(BYTES_PER_SAMPLE)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(all_samples.tobytes())

    print(f"Saved {len(all_samples)} mono samples to {OUTPUT_WAV_FILE}")

if __name__ == "__main__":
    main()
