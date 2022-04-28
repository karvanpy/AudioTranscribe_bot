import os
from pydub import AudioSegment
import speech_recognition as sr
# filewav = '../samples/greetings.wav'

def transcribe(audiofile, language='id-ID'):
    if audiofile.endswith('.ogg'):
        f = audiofile.replace('.ogg', '.wav')
        convert = AudioSegment.from_file(audiofile)
        convert.export(f, format='wav')
        audiofile = f

    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audiofile)
    with audio_file as source:
        data = recognizer.record(source)
        
    text = recognizer.recognize_google(data, language=language)

    os.remove(f)
    
    return text