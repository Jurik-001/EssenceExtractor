"""Extracts audio from a video file and transcribes it to text."""

import os

import speech_recognition as sr
import whisper
from moviepy.editor import AudioFileClip

from src import utils


class Transcriber:
    """Extracts audio from a video file and transcribes it to text."""

    def __init__(self, output_path="audios"):
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.transcribe_model = whisper.load_model("base")
        self.token_counter = utils.TokenCounter()

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
        
    def split_audio_into_token_chunks(self, transcript_result, chunk_size=200):
        """Split audio into chunks of equal length or silence."""
        chunks = []
        chunk = ""
        start_time = 0
        for segment in transcript_result["segments"]:
            if segment["text"] == "":
                print("Silence")
                continue
                
            tokens = self.token_counter.count_tokens(chunk+segment["text"])
            if tokens > chunk_size:
                chunks.append({"chunk": chunk, "start_time": start_time})
                chunk = ""
                start_time = segment["end"]
            else:
                chunk += segment["text"]
        return chunks
    
    def _assemble_transcript(self, chunks):
        """Assemble transcript from chunks."""
        assemble_text = ""
        for chunk in chunks:
            minutes = int(chunk['start_time'] // 60)
            seconds = int(chunk['start_time'] % 60)
            assemble_text += f"[{minutes:02d}:{seconds:02d}]{chunk['chunk']} "

        return assemble_text

    def transcribe_audio(self, audio_file_path):
        """Transcribes audio to text.

        Args:
            audio_file_path (str): The path to the audio file.

        Returns:
            str: The path to the transcription file.
        """
        transcript_result = self.transcribe_model.transcribe(audio_file_path)
        token_chunks = self.split_audio_into_token_chunks(transcript_result)
        assemble_text = self._assemble_transcript(token_chunks)

        transcription_file_path = audio_file_path.replace(".wav", ".txt")

        with open(transcription_file_path, "w") as f:
            f.write(assemble_text)

        return transcription_file_path


