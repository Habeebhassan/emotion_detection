from pydub import AudioSegment

# Convert an MP3 file to WAV
audio = AudioSegment.from_mp3("/Users/mac/Downloads/town-10169.mp3")
audio.export("/Users/mac/Downloads/output_audio_file.wav", format="wav")