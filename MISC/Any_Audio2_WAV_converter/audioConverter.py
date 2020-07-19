from pydub import AudioSegment

audio_location = input()
audio_format = audio_location.split(".")[1]


wav_audio = AudioSegment.from_file(audio_location, format=audio_format)

wav_audio.export("audio1.wav", format="wav")
