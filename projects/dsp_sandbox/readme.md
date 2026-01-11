
# Digital Signal Processing (DSP) Sandbox 

A real-time Digital Signal Processing (DSP) sandbox for generating, visualizing, and analyzing waveforms in the time and frequency domains.

## Features

* **Signal Generation**: Create Sine, Square, and Sawtooth waves with adjustable frequency (1 Hz to 1000 Hz), phase, and Gaussian noise.
* **Oscilloscope View**: Real-time time-domain plot with a "Cycles to Display" feature to zoom into specific wave periods. 
* **Spectrum Analyzer**: Magnitude and Phase analysis using Fast Fourier Transform (FFT).
* **Engineering Metrics**: Automatic peak frequency detection and Total Harmonic Distortion (THD) calculation.
* **DSP Tools**: Toggleable Hann windowing and Logarithmic (dB) scaling for the magnitude spectrum.
* **Data Export**: Save frequency and magnitude data directly to CSV for external analysis.

---

## Requirements

* Python 3.x
* `numpy`
* `matplotlib`
* `tkinter` (Standard Python library)

---

## Installation

Install the necessary dependencies using pip:

```bash
pip install numpy matplotlib

```

---

## Usage

1. **Run the Script**:
```bash
python main.py

```


2. **Frequency Control**: Use the slider to set the fundamental tone. For 1 Hz analysis, set the slider to minimum.
3. **Cycles to Display**: Adjust this slider to 1 to see a single full wave period, or increase it to see multiple wave repetitions.
4. **Analysis Mode**: Switch between **Magnitude** and **Phase**.
5. **Exporting**: Click **Export CSV** to save the frequency bins and magnitude values for use in Excel or MATLAB.

---

## Technical Specifications

| Parameter | Value |
| --- | --- |
| Sampling Rate | 30,000 Hz |
| Buffer Duration | 10.0 seconds |
| FFT Resolution | 0.1 Hz per bin |
| Frequency Range | 0 Hz to 15,000 Hz (Nyquist) |
| Scaling | Automatic intelligent zoom based on target frequency |

---