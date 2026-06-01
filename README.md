This is the code for the first iteration of my project to solve the "cocktail party problem".

From Wikipedia:

> "The cocktail party effect refers to a phenomenon wherein the brain focuses a person's attention on a particular stimulus, usually auditory.
> This focus excludes a range of other stimuli from conscious awareness, as when a partygoer follows a single conversation in a noisy room.
> This ability is widely distributed among humans, with most listeners more or less easily able to portion the totality of sound detected by the ears into distinct streams,
> and subsequently to decide which streams are most pertinent, excluding all or most others...
> A person who lacks the ability to segregate stimuli in this way is often said to display the cocktail party problem or cocktail party deafness.
> This may also be described as auditory processing disorder or King-Kopetzky syndrome."

## Hardware Target

- STM32L475-based development board
- Two onboard MP34DT01 PDM microphones
- Microphone spacing: approximately 21 mm
- Audio capture through DFSDM
- UART streaming over USART1 at 921600 baud

At a 16 kHz audio sample rate, one sample period corresponds to about 21.4 mm of sound travel. Because the microphones are spaced about 21 mm apart, a one-sample delay is the most physically meaningful delay for first-pass two-microphone beamforming experiments.

## Current Main Branch Behavior

The `main` branch currently captures both microphones, applies a simple one-sample delay-and-sum beamformer, and streams the result as mono audio.

The firmware flow is:

1. DFSDM captures two microphone channels into DMA buffers.
2. Each raw DFSDM sample is scaled and clamped to 16-bit PCM.
3. Mic 1 is delayed by one sample.
4. Mic 0 and delayed Mic 1 are averaged.
5. The resulting mono beamformed frame is sent over UART using DMA.

The current UART output format on `main` is:

```text
1 channel
512 int16 samples per frame
1024 bytes per frame
Intended sample rate: 16 kHz
```

To record the beamformed version, use:

```powershell
python Core\Src\beamformed_stream.py
```

## Stereo Non-Beamformed Branch

There is a separate branch for recording the raw two-microphone stereo stream:

```text
stereo-non-beamformed
```

That branch records true interleaved stereo with no beamforming:

```text
mic0, mic1, mic0, mic1, ...
```

The matching receiver script for that branch is:

```powershell
python Core\Src\audio_stream.py
```

The stereo stream format is:

```text
2 channels
1024 interleaved int16 samples per frame
2048 bytes per frame
Intended sample rate: 16 kHz
```

## Example Recordings

`Core/Src/received_audio_w_beamforming.wav` and `Core/Src/received_audio_wo_beamforming.wav` are example recordings of speaking in front of the microphones on the board while music plays in the background. They demonstrate how background audio is attenuated when beamforming is enabled.
