#!/usr/bin/env python3

import json
import sys
import signal
import os.path
import argparse
import datetime
import librosa
import numpy as np

###############
#  Arguments  #
###############
parser = argparse.ArgumentParser()

parser.add_argument('input',
                    help='Directory with audio files to be analyzed (read is recursive)')

parser.add_argument('-o', '--output',
                    help='Optional path to json output (defaults to current directory)')

args = parser.parse_args()

def signal_handler(signum, frame):
  print('Interrupted')
  sys.exit(0)

# Handle C-c
signal.signal(signal.SIGINT, signal_handler)

##############
#  Analysis  #
##############
def analyze(files):
  """
  Audio feature extraction
  """
  output = []

  for file in files:
    # Load the audio as a waveform `y`
    # Store the sampling rate as `sr`
    y, sr = librosa.load(file)

    # spectral centroid
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    # spectral bandwidth
    spectral_bandwidths = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    # mel-frequency cepstral coefficients
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    mfccs = librosa.feature.spectral.mfcc(y=y, sr=sr, S=librosa.core.logamplitude(S), n_mfcc=12)
    # duration
    duration = librosa.core.get_duration(y=y, sr=sr)

    json_data = {
      'path': file,
      'duration': duration,
      'spectral_centroids': spectral_centroids[0].tolist(),
      'spectral_bandwidths': spectral_bandwidths[0].tolist(),
      'spectral_centroid_min': spectral_centroids.min(),
      'spectral_centroid_max': spectral_centroids.max(),
      'spectral_centroid_mean': spectral_centroids.mean(),
      'mfccs': mfccs.tolist(),
      'mfcc_mean': mfccs.mean(),
    }

    print('Analyzing file:', file)
    output.append(json_data)

  return output;

if not args.input:
  print('No input path specified, see --help')
  sys.exit()

# Get paths for audio files
valid_extensions = ['aac', 'au', 'flac', 'm4a', 'mp3', 'ogg', 'wav', 'aif']
audio_file_path = os.path.expanduser(args.input)

if os.path.isdir(audio_file_path):
  audio_files = librosa.util.find_files(audio_file_path,
                                        ext=valid_extensions)
else:
  audio_files = [ audio_file_path ]

# do the analysis
result = analyze(audio_files)

#########
#  I/O  #
#########
def parse_input():
  """
  Parse user input to determine if we should overwrite the existing file
  """
  # raw_input returns the empty string for "enter"
  yes = set(['yes','y', 'ye', ''])
  no = set(['no','n'])
  choice = input('-> ').lower()

  while True:
    if choice in yes:
      return True
    elif choice in no:
      return False
    else:
      sys.stdout.write("Please respond with 'yes' or 'no'")


def write_file(path, data):
  """
  Write data to file
  """
  with open(path, 'w') as file:
    json.dump(data, file, separators=(',', ':'))

  print('Wrote output to', path)

if args.output:
  json_path = os.path.expanduser(args.output)
else:
  json_path = os.path.abspath('./output.json')

# json document structure
json_output = {
  'files': result,
  'timestamp': datetime.datetime.now().isoformat(),
  'version': '0.1'
}

if os.path.isfile(json_path):
  print('File {0} exists'.format(json_path))
  print('Overwrite?\n y/n')
  overwrite = parse_input()
  if overwrite:
    write_file(json_path, json_output)
  else:
    print('File was not overwritten')
else:
  write_file(json_path, json_output)

