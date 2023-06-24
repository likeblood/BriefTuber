import os
import re
import json

from pytube import YouTube

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from google.oauth2 import service_account


class Video2TextPipeline:

    def __init__(self, video_link: str) -> None:
        self.video_link: str = video_link
    
    def sanitize_filename(self, filename):
        filename = re.sub(r'[\/:*?"<>|]', '', filename)
        return filename

    def download_audio(self, url):
        youtube = YouTube(url)
        video = youtube.streams.filter(only_audio=True).first()

        # Скачать только аудио без видео
        audio_stream = video.download()
        audio_file = self.sanitize_filename(video.title) + ".mp3"

        # Переместить загруженный файл
        os.rename(audio_stream, audio_file)
        
        return audio_file
        
    def transcribe_audio(self, audio_file):
        # Создать клиент для Cloud Storage
        credentials = service_account.Credentials.from_service_account_file('PATH')
        storage_client = storage.Client(credentials=credentials)

        # Загрузить аудиофайл в Cloud Storage
        bucket_name = "speech-to-text-qwerty"  
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob("audio.mp3")  
        blob.upload_from_filename(audio_file)

        # Получить URI загруженного файла
        audio_uri = f"gs://{bucket_name}/{blob.name}"

        client = speech.SpeechClient()

        # Создать объект RecognitionAudio с использованием URI файла
        audio = speech.RecognitionAudio(uri=audio_uri)

        #параметры распознавания
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code="ru-RU",
        )

        # Выполнить распознавание аудио
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result()

        # Обработать результат распознавания
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        # Создать словарь с результатом
        result_dict = {
            "transcript": transcript
        }

        # Преобразовать словарь в JSON
        result_json = json.dumps(result_dict)

        return result_json

    def clean_text(self) -> str:
        """
        Clean text from video.

        Returns:
            str: cleaned text
        """
        pass

    def make_summary(self) -> str:
        """
        Make summary from text.

        Returns:
            str: summary
        """
        pass

    def run(self) -> str:
        """
        Run pipeline

        Returns:
            str: summary
        """
        audio_path = self.download_text_from_video()
        text = self.convert_audio_to_text(audio_path)
        cleaned_text = self.clean_text(text)
        summary = self.make_summary(cleaned_text)
        return summary
