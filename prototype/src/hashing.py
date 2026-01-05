import numpy as np
import argparse
from spectrogram import load_audio, generate_spectrogram
from peaks import find_peaks
min_peak_seperation=10
max_peak_seperation=100
fan_out=10
def peak_to_coordinates(mask:np.ndarray) -> np.ndarray:
    #To convert the boolean mask into a array sorted by time as[time,freq]
    #1) for the coordinates:
    #since the spectrogram is of frequency and time theb argwhere return (freq,time)
    coords=np.argwhere(mask)

    #2)SWap the values to get (time,freq)
    # You prioritize Time because audio is a time-series.
    coords=coords[:,[1,0]]
    #FInally sort the array based upon time
    coords=coords[coords[:,0].argsort()]

    return coords

def generate_hashes(peaks:np.ndarray) -> list:
    """
    Generates (hash, time_offset) tuples.
    peaks: Array of [time_idx, freq_idx] sorted by time.
    """
    hashes = []

    #for every peak in the spectrogram
    for i in range(len(peaks)):
        t1,f1=peaks[i]
        pair_count=0
        for j in range(i+1,len(peaks)):
            t2,f2=peaks[j]
            t_delta=t2-t1

            #to avoid the immediate neighbours(constraint1):
            if t_delta<min_peak_seperation:
                continue
            #to get only the peaks within the window(constraint2):
            if t_delta>max_peak_seperation:
                break
            #To get the values within the Fanout only(constrint 3):
            if pair_count>=fan_out:
                break
            

            #create the hash key and store it in the list of hsahes
            h=(f1,f2,t_delta)
            hashes.append((h,t1))

            pair_count+=1

    return hashes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input audio")
    args = parser.parse_args()
    
    print(f"Processing {args.input_file}...")
    
    # 1. Pipeline: Audio -> Spectrogram -> Peaks
    audio = load_audio(args.input_file)
    S_db = generate_spectrogram(audio)
    peaks_mask = find_peaks(S_db)
    
    # 2. Convert Mask to Coords
    peak_coords = peak_to_coordinates(peaks_mask)
    print(f"[-] Total Peaks Found: {len(peak_coords)}")
    
    # 3. Generate Hashes
    print("[-] Generating Hashes...")
    fingerprints = generate_hashes(peak_coords)
    
    print("-------------------------------")
    print(f"Total Hashes:     {len(fingerprints)}")
    if len(peak_coords) > 0:
        print(f"Hashes per Peak:  {len(fingerprints) / len(peak_coords):.2f}")
    print("-------------------------------")
    
    # Verification (Show the first 5 hashes)
    print("Sample Fingerprints (f1, f2, dt):")
    for i in range(min(5, len(fingerprints))):
        print(f"  {fingerprints[i][0]} @ Time {fingerprints[i][1]}")

if __name__ == "__main__":
    main()
