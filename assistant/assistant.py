import speech_recognition as sr
import pprint
import os
import socket
import sys


## TODO this didnt work to turn off Jack and alsa error messages
stderr = sys.stderr
def turn_off_stderr():
  global stderr
  sys.stderr = None

def turn_on_stderr():
  sys.stderr = stderr


def onPi99():
  hostname = socket.gethostname() 
  return hostname == 'pi99'



def recognize_local_files():
  r = sr.Recognizer()
  audioDir = 'test_audio'
  for filename in os.listdir(audioDir):
    if not filename.endswith('.wav'):
      continue
    filepath = os.path.join(audioDir, filename)
    test_file = sr.AudioFile(filepath)
    with test_file as source:
      audio = r.record(source)
      res = r.recognize_sphinx(audio)
      print("{}: {}".format(filepath, res))

def get_microphones():
  mic = sr.Microphone()
  return mic.list_microphone_names()

def get_steinberg_mic():
  print("Getting microphone for steinberg interface...")
  mic_names = get_microphones()
  for index, name in enumerate(mic_names):
    if 'UR816C' in name:
      return index



def get_pi_mic():
  print("Getting microphone for raspberry pi...")
  mic_names = get_microphones()
  for index, name in enumerate(mic_names):
    if 'USB' in name:
      return index

def transcribe_loop():
  mic_index = get_pi_mic() if onPi99() else get_steinberg_mic()
  mic = sr.Microphone(device_index=mic_index)

  while(True):
    recognizer = sr.Recognizer()
    with mic as source:
      print("Adjusting for ambient noise...")
      recognizer.adjust_for_ambient_noise(source)
      print("Listening for audio...")
      audio = recognizer.listen(source)

    try:
      print("Transcribing...")
      transcript = recognizer.recognize_sphinx(audio)
      print(transcript)
    except:
      print("No transcriptions found") 

transcribe_loop()