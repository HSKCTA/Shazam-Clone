#pragma once
#include <vector>
#include <complex>
#include <fftw3.h>
#include <cmath>

class Spectrogram{
public:
    //Same constants a the one one in the python implementation (The basic required values)
    static const int SAMPLE_RATE=44100;
    static const int N_FFT=2048;
    static const int HOP_LENGTH=1024;

    Spectrogram();
    ~Spectrogram();

    //The main API : TAkes raw audio and returns the 2D Spectrogram
    std::vector<std::vector<double>> generate(const std::vector<double>& audio);

private:
    //FFTW Resources
    fftw_complex* fft_in;
    fftw_complex* fft_out;
    fftw_plan plan;

    // Helper: Hanning Window
    std::vector<double> window;
    void build_hanning_window();
};