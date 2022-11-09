import os
import wave
import pyaudio
import collections
from fuzzywuzzy import fuzz
import speech_recognition as sr
from speech_recognition import Microphone

command = collections.namedtuple('Command', ["input", "filepath"])

def play_audio(file:str):
    CHUNK = 1024
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data):
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

def callback(r, audio):
    try:
        recognized = r.recognize_google(audio)
        how_close = fuzz.ratio(recognized, "Hey Quarishma")
        print(how_close)
        if how_close >= 60:
            print("Doing Stuff")
            command_recog = sr.Recognizer()
            command_mic = Microphone()
            with command_mic:
                command_recog.adjust_for_ambient_noise(command_mic)
                play_audio(os.path.join('audios', "what_can_i_do.wav"))
                command_audio = command_recog.record(command_mic, 3)
            try:
                possible_commands = [
                    command("Can you give me the latest news", "latest_news.py"),
                    command("What is your name", "my_name")
                ]
                recognized_command = command_recog.recognize_google(command_audio)
                for comm in possible_commands:
                    if fuzz.ratio(recognized_command, comm.input) >= 60:
                        os.system(f"python commands/{comm.filepath}")
                print(recognized_command)
            except Exception as e:
                play_audio(os.path.join('audios', "not_get.wav"))
                print(f"Error: {e}")
        print(recognized)
    except Exception as e:
        print(f"Couldn't recognise the audio: {e}")

def listen():
    r = sr.Recognizer()
    mic = Microphone()
    with mic:
        r.adjust_for_ambient_noise(mic, 5)
    print("Start")
    r.listen_in_background(mic, callback)

listen()
while True:
    pass