import numpy as np
import argparse
from scipy.ndimage import maximum_filter
from spectrogram import load_audio, generate_spectrogram

def find_peaks(S_db:np.ndarray) -> np.ndarray :
    #the size of area where the peak should be found in 
    neighborhood_size=(20,20)
    #function to find the max in the region
    local_max=maximum_filter(S_db,size=neighborhood_size)
    #Boolean Mask
    is_peak=(S_db==local_max)
    #for threshold(floor) value :- anything that's less than the max peak-80db
    global_max=np.max(S_db)
    noise_floor=global_max-80
    is_loud=(S_db>noise_floor)
    #Final check for the peak (must be loud enough and should be a peak as well of the region)
    detected_peaks=is_peak & is_loud

    return detected_peaks 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input audio")
    args = parser.parse_args()
    
    print(f"Loading {args.input_file}...")
    audio = load_audio(args.input_file)
    S_db = generate_spectrogram(audio)
    
    print("Finding peaks...")
    peaks_mask = find_peaks(S_db)

    #Count the true values 
    peak_count=np.sum(peaks_mask)

    print("-------------------------------")
    print(f"Spectrogram Size: {S_db.size} pixels")
    print(f"Peaks Found:      {peak_count}")
    print(f"Reduction Ratio:  {S_db.size / peak_count:.1f}x")
    print("-------------------------------")

if __name__ == "__main__":
    main()