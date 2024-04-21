from autocorrect import Speller


def convert_speech(audio_path):
    from backend.global_declarations import model

    transcriptions = model.transcribe([audio_path])

    spell = Speller('ru')
    return spell(transcriptions[0]["transcription"])
