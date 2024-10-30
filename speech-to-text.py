import assemblyai as aai

aai.settings.api_key = "96452f4e5a3e4d2c8f6ac2d7ff6f9485"

transcriber = aai.Transcriber()

# You can use a local filepath:
# audio_file = "./example.mp3"

# Or use a publicly-accessible URL:
audio_file = (
    "https://assembly.ai/sports_injuries.mp3"
)

config = aai.TranscriptionConfig(speaker_labels=True)

transcript = transcriber.transcribe(audio_file, config)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

print(transcript.text)

for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")


# import assemblyai
# import time

# # Initialize AssemblyAI client with your API key
# API_KEY = "96452f4e5a3e4d2c8f6ac2d7ff6f9485"  # Replace with your actual API key
# client = assemblyai.Client(api_key=API_KEY)

# # Path to the audio file you want to transcribe
# audio_file_path = "/Users/mac/Downloads/town-10169.mp3"  # Replace with your actual file path

# # Step 1: Upload the audio file
# def upload_audio(file_path):
#     upload_url = client.upload(file_path)
#     return upload_url

# # Step 2: Request transcription
# def request_transcription(upload_url):
#     transcript = client.transcribe(audio_url=upload_url)
#     return transcript

# # Step 3: Retrieve the transcription result
# def get_transcription_result(transcript):
#     while not transcript.done:
#         time.sleep(3)  # Wait a few seconds before checking again
#         transcript = transcript.refresh()
#     if transcript.error:
#         raise Exception("Transcription failed.")
#     return transcript.text

# # Run the transcription process
# try:
#     upload_url = upload_audio(audio_file_path)
#     transcript = request_transcription(upload_url)
#     transcript_text = get_transcription_result(transcript)
#     print("Transcript:", transcript_text)
# except Exception as e:
#     print("Error:", e)


# import requests
# import time

# # Set your AssemblyAI API key
# API_KEY = "96452f4e5a3e4d2c8f6ac2d7ff6f9485"  # Replace with your actual API key

# # Path to the audio file you want to transcribe
# audio_file_path = "/Users/mac/Downloads/town-10169.mp3"  # Replace with your actual file path

# # Headers for authentication
# headers = {
#     "authorization": API_KEY,
#     "content-type": "application/json"
# }

# # Step 1: Upload the audio file
# def upload_audio(file_path):
#     with open(file_path, "rb") as audio_file:
#         response = requests.post(
#             "https://api.assemblyai.com/v2/upload",
#             headers=headers,
#             files={"file": audio_file}
#         )
#     response.raise_for_status()
#     return response.json()["upload_url"]

# # Step 2: Request transcription
# def request_transcription(upload_url):
#     json_data = {
#         "audio_url": upload_url
#     }
#     response = requests.post(
#         "https://api.assemblyai.com/v2/transcript",
#         headers=headers,
#         json=json_data
#     )
#     response.raise_for_status()
#     return response.json()["id"]

# # Step 3: Retrieve the transcription result
# def get_transcription_result(transcript_id):
#     polling_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
#     while True:
#         response = requests.get(polling_url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         if data["status"] == "completed":
#             return data["text"]
#         elif data["status"] == "failed":
#             raise Exception("Transcription failed.")
#         time.sleep(3)  # Wait a few seconds before polling again

# # Run the transcription process
# try:
#     upload_url = upload_audio(audio_file_path)
#     transcript_id = request_transcription(upload_url)
#     transcript_text = get_transcription_result(transcript_id)
#     print("Transcript:", transcript_text)
# except Exception as e:
#     print("Error:", e)