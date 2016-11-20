Audio feature extraction
========================

**Note: This is a work in progress**

Requirements
------------

* Python3
* [librosa](https://github.com/librosa/librosa)

Description
-----------

Tool for extracting spectral features (MFCC, bandwidth, centroid) from a given set of audio files.

Usage
-----

    usage: audio-feature-extraction.py [-h] [-i INPUT] [-o OUTPUT]

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                            Directory with audio files to be analyzed (read is
                            recursive)
    -o OUTPUT, --output OUTPUT
                            Optional path to json output (defaults to current
                            directory)

Example

    ./audio-feature-extraction.py -i ~/audio/test-files -o ~/audio/test-files/features.json
