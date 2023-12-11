from unittest.mock import patch
from essence_extractor import Transcriber



@patch('essence_extractor.src.transcriber.AudioFileClip')
def test_extract_audio(mock_audio_file_clip):
    mock_audio_file_clip.return_value.write_audiofile = lambda x: None
    transcriber = Transcriber("test_output")
    audio_file_path = transcriber.extract_audio("test_video.mp4")
    assert audio_file_path == "test_output/test_video.wav"


def test_split_audio_into_token_chunks():
    transcriber = Transcriber("test_output")
    transcript_result = {
        "segments": [
            {"text": "Hello ", "end": 5},
            {"text": "world", "end": 10}
        ]
    }
    chunks = transcriber.split_audio_into_token_chunks(transcript_result, chunk_size=2)
    assert len(chunks) > 0


def test_assemble_transcript():
    transcriber = Transcriber("test_output")
    chunks = [{"chunk": "Hello world", "start_time": 0}]
    assembled_transcript = transcriber._assemble_transcript(chunks)
    assert assembled_transcript.startswith("[00:00]Hello world")



