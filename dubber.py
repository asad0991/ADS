input_filepath="static/uploads/"
output_filepath = "~/Transcripts/"
bucketname = "dubbing-speech-to-text-bucket2"
from googletrans import Translator
from pydub import AudioSegment
import os
from google.cloud import speech
import wave
from google.cloud import storage
import google.cloud.texttospeech as tts
import moviepy.editor as mp
from ssml_builder.core import Speech
import db_conn
import app
from pytube import YouTube

def download_video(link):
    # create a YouTube object
    yt = YouTube(link)

    # get the highest resolution video stream
    stream = yt.streams.get_highest_resolution()

    # download the video
    output_path = "static/uploads"
    stream.download(output_path=output_path)
    return yt.title + '.mp4'

def extract_audio(filename):

    """Extracting the audio from video using moviepy"""

    my_clip = mp.VideoFileClip(input_filepath + filename)
    my_clip
    my_clip.audio.write_audiofile("motiv.wav")



def stereo_to_mono(audio_file_name):
    """Converting the audio stream to mono if its stereo"""

    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    """fetching the framerate of the extracted audio clip"""

    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the Google Cloud bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()


def audio_to_text(audio_file_name,original_language,target_language):
    """Converting the audio to text by Google's Speech to Text Api"""

    file_name = audio_file_name
    frame_rate, channels = frame_rate_channel(file_name)

    """Checking if the audio stream is stereo or mono. If its stereo it will be converted to mono"""

    if channels > 1:
        stereo_to_mono(file_name)

    bucket_name = bucketname
    source_file_name = audio_file_name
    destination_blob_name = audio_file_name

    """Passing the required parameters to Upload Blob Function to upload audio file to Google cloud bucket """

    upload_blob(bucket_name, source_file_name, destination_blob_name)


    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    """Setting the parameters for the speech tp text API """
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=original_language,
        enable_word_time_offsets=True,
    )
    """Passing the audio and configuration to the API"""
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=10000)
    print(response)
    """Deleting the audio file from google cloud bucket"""

    delete_blob(bucket_name, destination_blob_name)
    stamp = 0.0

    """Using ssml for text to speech"""

    sp = Speech()

    """Grouping the response text in sentences and passing them to the text translation API"""

    sentence = ''
    alternative = response.results[0].alternatives[0]
    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time
        if stamp == 0.0:

            """Adding Pauses in dubbed audio according to the source video """

            sp.pause(time=end_time.total_seconds())
            stamp = end_time.total_seconds()
            sentence += word
        elif stamp == start_time.total_seconds():
            sentence += ' ' + word
            stamp = end_time.total_seconds()
        elif stamp != start_time.total_seconds():
            """Translating a single sentence"""
            sentence = text_translation(sentence, original_language, target_language)
            """Adding the sentence to ssml"""
            sp.add_text(sentence)
            """Adding Pauses in dubbed audio according to the source video """
            sp.pause(time=start_time.total_seconds() - stamp)
            sentence = ''
            sentence += word
            stamp = end_time.total_seconds()
    sentence = text_translation(sentence,original_language,target_language)
    sp.add_text(sentence)
    """Storing the finalized ssml in a variable """
    ssml = sp.speak()
    return ssml


def text_translation(content,original_language,target_language):

    """Extracting the language code from the variables"""

    original_language=original_language.split('-',1)
    target_language=target_language.split('-',1)
    print(original_language)
    print(target_language)
    """Translating the text content"""
    file_translate = Translator()
    result = file_translate.translate(content, dest=target_language[0], src=original_language[0])
    print(result.text)
    res = result.text

    return res

def text_to_audio(voice_name: str,original_language, ssml: str,video_file, email):

    """Setting the configuration for tts API"""

    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(ssml=ssml)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name, ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16, speaking_rate=0.9)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )
    target_language=''
    if language_code == 'en-GB':
        target_language = "English"
    elif language_code == 'yue-HK':
        target_language = 'Chinese'
    elif language_code == 'ru-RU':
        target_language = 'Russian'
    elif language_code == 'hi-IN':
        target_language = 'Hindi'

    language_code = original_language
    if language_code == 'en-GB':
        original_language = "English"
    elif language_code == 'yue-HK':
        original_language = 'Chinese'
    elif language_code == 'ru-RU':
        original_language = 'Russian'
    elif language_code == 'ur-PK':
        original_language = 'Urdu'


    """Stitching the generated audio on the video"""

    filename = f"{language_code}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
    audio= mp.AudioFileClip(filename)
    my_clip = mp.VideoFileClip( input_filepath + video_file )
    new=my_clip.without_audio()
    new = new.set_audio(audio)

    new.write_videofile("static/dubbed/Dubbed-" + video_file, fps=30, threads=1, codec="libx264" )
    with app.app.app_context():
        video_id=db_conn.insert_video("static/dubbed/Dubbed-" + video_file,original_language, target_language, email)

    return video_id

def dub_video(filename,original_language,target_langauge, email):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'
    extract_audio(filename)
    return text_to_audio(target_langauge,original_language, audio_to_text("motiv.wav",original_language,target_langauge),filename, email)

