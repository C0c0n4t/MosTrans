from huggingsound import SpeechRecognitionModel
from autocorrect import Speller

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian")
audio_paths = ["me.wav"]

transcriptions = model.transcribe(audio_paths)

spell = Speller('ru')
print(spell(transcriptions[0]["transcription"]))
