# Audio Engine Specifications

## Signal Processing
- **Sample Rate (SR):** 44100 Hz (Standard PCM)
- **Channels:** Mono (Stereo adds unnecessary complexity for fingerprinting; we will average channels)
- **Data Type:** 32-bit Floating Point (PCM)

## Short-Time Fourier Transform (STFT)
- **Window Function:** Hann (Hanning) Window
  - *Why:* Reduces spectral leakage compared to a rectangular window.
- **FFT Size (N_FFT):** 2048 samples
  - *Resolution:* ~21.5 Hz per bin ($SR / N_{FFT}$).
  - *Duration:* ~46ms per frame.
- **Hop Length:** 1024 samples
  - *Overlap:* 50%
  - *Why:* 50% overlap balances temporal resolution with CPU load. Less overlap = missed transient peaks. More overlap = redundant data/high load.
