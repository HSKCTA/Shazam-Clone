import argparse
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
SAMPLE_RATE=44100
N_FFT=2048
HOP_LENGTH=1024

def load_audio(file_path: str)->np.ndarray:
    try:
        y,_=librosa.load(file_path,sr=SAMPLE_RATE,mono=True )
        return y
    except Exception as e:
        print(f"Failed to load audio : {e}")
        exit('1')

def generate_spectrogram(audio_array:np.ndarray):
   #short time fourier transform(stft) returns the complex matrix
   D= librosa.stft(audio_array,n_fft=N_FFT,hop_length=HOP_LENGTH,window='hann')

   #Calculation to magnitude from complex no.s
   S=np.abs(D)


   #Converting the raw amplitude for proper visualisation
   S_db=librosa.amplitude_to_db(S,ref=np.max)
   return S_db

def plot_spectrogram(S_db:np.ndarray,output_file:str):
    plt.figure(figsize=(12,6))
    librosa.display.specshow(S_db,sr=SAMPLE_RATE,hop_length=HOP_LENGTH,x_axis='time',y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f' Spectrogram (N_FFT={N_FFT}Hop={HOP_LENGTH})')
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Spectrogram saved to {output_file}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("input_file",help="Path to input .wv/.mp3 file")
    parser.add_argument("--output",default="Spectrogram_debug.png",help="Output image path")
    args=parser.parse_args()
    print(f"Processing  {args.input_file}...")
    audio=load_audio(args.input_file)
    spectrogram=generate_spectrogram(audio)

    print(f"[-] Audio Samples:{len(audio)}")
    print(f"[-]Spectrogram SHape (Freq Bins,Time Frames):{spectrogram.shape}")

    plot_spectrogram(spectrogram,args.output)

if __name__=="__main__":
    main()


    