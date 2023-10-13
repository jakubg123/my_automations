from google.oauth2 import service_account
from google.cloud import speech
import io
import sys
import os
from pytube import YouTube
from moviepy.editor import *
import openai



def download_youtube_video_as_wav(youtube_url, output_path):
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path, filename="temp")

    print("mp4-->wav")
    video_path = f"{output_path}/temp"
    audio = AudioFileClip(video_path)
    audio.write_audiofile(f"{output_path}/output.wav")
    os.remove(video_path)
    return f"{output_path}/output.wav"

def split_audio(file_path, output_path, segment_length=30):
    audio = AudioFileClip(file_path)
    total_length = audio.duration
    segments = []
    for i in range(0, int(total_length), segment_length):
        segment_file = f"{output_path}/segment_{i}.wav"
        audio.subclip(i, i+segment_length).write_audiofile(segment_file)
        segments.append(segment_file)

    return segments

def transcribe_audio(audio_path):
    client_file = 'key.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    with io.open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
    

    config = speech.RecognitionConfig(
        audio_channel_count = 2,
        language_code='en-US'
    )
    response = client.recognize(config=config, audio=audio)

    transcript = ''

    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript



def get_top_takeaways(text, num_takeaways=5):
    API_KEY = open("API_KEY","r").read()
    open.api_key = API_KEY
    prompt = f"Analyze this text and give me the top {num_takeaways} takeaways: \"{text}\""

    response = openai.Completion.create(
      model="gpt-3.5-turbo",
      prompt=prompt,
    )

    return response.choices[0].text.strip()


if __name__ == '__main__':
    youtube_url = 'https://www.youtube.com/watch?v=7DCO-IISBnc'
    output_path = os.getcwd()

    audio_path = download_youtube_video_as_wav(youtube_url, output_path)
    audio_segments = split_audio(audio_path, output_path)
    transcripts = []
    for i, segment in enumerate(audio_segments, 1):
        print(f"Transcribing segment {i}/{len(audio_segments)}...")
        transcript = transcribe_audio(segment)
        transcripts.append(transcript)

    full_transcript = ' '.join(transcripts)
    # with open(f"{output_path}/full_transcript.txt", 'w') as transcript_file:
    #     transcript_file.write(full_transcript)

    # with open(f"{output_path}/full_transcript.txt", 'r') as file:
    #     lines = file.read()


    takeaways = get_top_takeaways(full_transcript,5)

    with open('mySaveFile.txt','w') as file:
        file.write(takeaways)

    #future editing ?