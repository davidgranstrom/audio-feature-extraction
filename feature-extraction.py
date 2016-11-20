#!/usr/bin/env python3

import json
import sys
import os.path
import argparse
import librosa
import numpy as np

def analyze(files, output):
  "extract features from file list input"

  for file in audio_files:
    # Load the audio as a waveform `y`
    # Store the sampling rate as `sr`
    y, sr = librosa.load(file)

    # centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    # onsets
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_frames = librosa.core.frames_to_time(onset_frames[:20], sr=sr)

    json_data = {
      'path': file,
      'spectral_min': spectral_centroid.min(),
      'spectral_max': spectral_centroid.max(),
      'spectral_mean': spectral_centroid.mean(),
      'onsets': onset_frames.tolist()
    }

    print('Analyzing file:', file)
    output.append(json_data)

  return;

# Get paths for audio files
audio_file_path = os.path.expanduser('~/audio/speech')
audio_files = librosa.util.find_files(audio_file_path,
                                      ext=['aac', 'au', 'flac', 'm4a', 'mp3', 'ogg', 'wav', 'aif'])
# store output
output = []
# do the analysis
analyze(audio_files, output)

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
    json.dump(data, file)

  print('Wrote output to', path)

json_path = os.path.abspath('./output.json')
json_output = { 'files': output }

if os.path.isfile(json_path):
  print('File {0} exists'.format(json_path))
  print('Overwrite?')
  print('y/n?')
  overwrite = parse_input()
else:
  write_file(json_path, json_output)
  sys.exit()

if overwrite:
  write_file(json_path, json_output)
else:
  print('File was not overwritten')

