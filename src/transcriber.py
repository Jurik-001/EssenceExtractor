"""Extracts audio from a video file and transcribes it to text."""

import os

import speech_recognition as sr
from moviepy.editor import AudioFileClip

from src import utils


class Transcriber:
    """Extracts audio from a video file and transcribes it to text."""

    def __init__(self, output_path="audios"):
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def extract_audio(self, video_file_path):
        """Extracts audio from a video file.

        Args:
            video_file_path (str): The path to the video file.

        Returns:
            str: The path to the extracted audio file.
        """
        try:
            video_clip = AudioFileClip(video_file_path)

            audio_file_path = os.path.join(
                self.output_path, os.path.basename(video_file_path).replace("mp4", "wav"),
            )

            video_clip.write_audiofile(audio_file_path)
            return audio_file_path

        except Exception as e:
            utils.logging.error("An error occurred:", str(e))
            return None

    def transcribe_audio(self, audio_file_path):
        """Transcribes audio to text.

        Args:
            audio_file_path (str): The path to the audio file.

        Returns:
            str: The path to the transcription file.
        """
        try:
            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_file_path) as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_whisper(audio)
            transcription_file_path = audio_file_path.replace(".wav", ".txt")

            with open(transcription_file_path, "w") as f:
                f.write(text)
            return transcription_file_path

        except Exception as e:
            utils.logging.info("An error occurred:", str(e))
            return None
