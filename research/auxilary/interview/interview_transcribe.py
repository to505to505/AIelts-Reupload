import pydub
from pydub import AudioSegment
from pytubefix import YouTube


import os
import textwrap

from openai import OpenAI



pydub.AudioSegment.ffmpeg = "/opt/homebrew/bin/ffmpeg"



# openai
client = OpenAI(api_key='')


# prompt for audio
promptAudio = "Сейчас будет проведено интервью на русском для анализа рынка IETLS."



# get transcribe
def transcribe(file):
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=file,
    response_format="verbose_json",
  prompt=promptAudio,
  temperature=0.4,
  timestamp_granularities=["word"]
  
)
    return transcription


# split text for normal output 
def split_text(text, width):
    return textwrap.wrap(text, width=width)


line_length = 80

# final function
def final_transcribe(filename, length): 
    audio = AudioSegment.from_file('audio_data/'+ filename)
    counter = 0
    while len(audio)>length:
        audio_new = audio[0:length]
        audio_new.export(f"audio_data/segment_{counter}.mp3", format="mp3")
        audio = audio[length:]
        counter +=1

    audio.export(f"audio_data/segment_{counter}.mp3", format="mp3")
    if os.path.exists('audio_data/OUTPUT.txt'):
        os.remove('audio_data/OUTPUT.txt')
    with open('audio_data/OUTPUT.txt', 'w') as file:
            file.write(filename + '\n')

    for i in range(counter+1):
        output = transcribe(file=open(f'audio_data/segment_{i}.mp3', 'rb'))
        with open('audio_data/OUTPUT.txt', 'a') as file:
            lines = split_text(output.text, line_length)
            for line in lines:
                file.write(line + '\n')
        os.remove(f'audio_data/segment_{i}.mp3')

    
if __name__ == "__main__":
    final_transcribe('Matvei.m4a', 1400000)

    

