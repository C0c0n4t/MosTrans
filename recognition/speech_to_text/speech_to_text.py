from autocorrect import Speller


def convert_speech(audio_path):
    """Converts file with `audio_path` name to string and autocorrects misspelling"""
    from backend.global_declarations import model

    transcriptions = model.transcribe([audio_path])

    spell = Speller('ru')
    return spell(transcriptions[0]["transcription"])
