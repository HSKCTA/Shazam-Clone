import argparse
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from spectrogram import load_audio, generate_spectrogram
from peaks import find_peaks
from hashing import peak_to_coordinates, generate_hashes

def fingerprint_file(file_path: str):
 """Runs the entire pipeline and cretes the hash dictionary"""
 print(f"[-]Creating the fingerprints{file_path}....")
 audio=load_audio(file_path)
 S_db=generate_spectrogram(audio)
 peak_mask=find_peaks(S_db)
 coords=peak_to_coordinates(peak_mask)
 hashes_list=generate_hashes(coords)


 #Convert the list of hashes into a dictionary for quicklookups
 # Key: Hash Tuple (f1, f2, dt)
 # Value: List of absolute times [t1, t2...]
 database={}
 for h,t in hashes_list:
  if h not in database:
   database[h]=[]
  database[h].append(t)
 return database,len(hashes_list)

def find_matches(db_hashes:dict, query_hashes:list):
 """
 First find the offset between the clip and the orignal audio
 """
 #List of all offsets found
 time_offsets=[]
 matches_count=0
 for q_hash,q_time in query_hashes:
  if q_hash in db_hashes:
   db_times=db_hashes[q_hash] 

   for db_time in db_times:
    offset=db_time-q_time
    time_offsets.append(offset)
    matches_count+=1
 return time_offsets,matches_count


def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("database_song",help="Path to orignal full song")
 parser.add_argument("query_clip",help="Path to query clip")
 args=parser.parse_args()

 #1First fingerprint the whole song into a database
 db_index, db_count=fingerprint_file(args.database_song)
 print(f"    Database SIze:{db_count} hashes")

 #2 Fingerprint the query clip (Kept it in list for iteration)
 print(f" Fingerprining the query....")
 #3 reusing the old codes but then convert it to list as it returns dicts
 audio=load_audio(args.query_clip)
 S_db=generate_spectrogram(audio)
 peaks_mask=find_peaks(S_db)
 coords = peak_to_coordinates(peaks_mask)
 query_hashes=generate_hashes(coords)
 print(f"   Query Size :  {len(query_hashes)})hashes ")

 #3. Finding the matches
 print("[-] Matching......")
 offsets, total_hits=find_matches(db_index,query_hashes)

 print(f"Raw hash Hits:{total_hits}") 

 if total_hits == 0:
  print("NO Matches Found.")
  return
 
 #4 Analyze the (Histogram)
 #The most common Offset is the true start time.
 c=Counter(offsets)
 top_offset,score = c.most_common(1)[0]

 #Convert the frames back to approximate seconds
 #Hop SIze 1024/44100 Hz = 0.0232 seconds per frame
 estimated_seconds=top_offset*(1024/44100.0)

 print("----------------------------------------------------------")
 print(f"Result:Match found!!!")
 print(f"Best Offset Score:{score} (This many hashes aligned)")
 print(f"Estimated Start time:{estimated_seconds:.2f} seconds")
 print("----------------------------------------------------------")
 plt.figure(figsize=(10, 4))
 plt.hist(offsets, bins=100)
 plt.title(f"Alignment Histogram (Spike at {estimated_seconds:.2f}s indicates Match)")
 plt.xlabel("Time Offset (Frames)")
 plt.ylabel("Count")
 plt.tight_layout()
 plt.savefig("match_debug.png")
 print("Histogram saved to match_debug.png")

if __name__ == "__main__":
    main()