#!bin/bash

# audio
# alias rawaudiostream='arecord -f S16_LE -c 1 -t raw'
# alias stream_to_vasinator='arecord -f cd -c 1 -t raw | oggenc - -r -C 1 | ssh vas@vasinator mplayer -'

# python dependencies
sudo apt-get install python3-all-dev  swig git libpulse-dev libasound2-dev python3-pyaudio 
sudo pip3 install pocketsphinx
sudo pip3 install SpeechRecognition
