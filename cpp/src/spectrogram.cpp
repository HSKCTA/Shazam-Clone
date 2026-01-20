#include "spectrogram.h"
#include <iostream>
#include <algorithm>
Spectrogram::Spectrogram(){
    //1. Allocating the FFTW Memory (Complex Input -> Complex Output)
    //nOTE: Complex input is used as it simplifies the math ,though real to complex would be faster
    fft_in =(fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N_FFT);
    fft_out=(fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N_FFT);

    //2. Creating the plan
    //FFTW_MEASURE tells FFTW To run tests to find the fastest math for my cpu
    plan=fftw_plan_dft_1d(N_FFT,fft_in,fft_out,FFTW_MEASURE);

    //3Build the window
    build_hanning_window();

}
void Spectrogram::build_hanning_window(){
    window.resize(N_FFT);
    for
}
