from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextEmotionAnalysisSerializer, AudioEmotionAnalysisSerializer
from .text_model import TextEmotionAnalysis
from .audio_model import AudioEmotionAnalysis
import assemblyai as aai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
import json
import os

# Path to your downloaded OAuth credentials file
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")
# Scopes required for the Generative Language API
SCOPES = ["https://www.googleapis.com/auth/generative-language.tuning", "https://www.googleapis.com/auth/cloud-platform"]


# View for Text Emotion Detection
class TextEmotionAnalysisView(APIView):
    def post(self, request):
        serializer = TextEmotionAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            # Process the text input using Gemini API
            input_text = serializer.validated_data.get('input_text')
            emotion_analysis_result = self.get_emotion_analysis(input_text)

            if "error" in emotion_analysis_result:
                return Response({"error": emotion_analysis_result["error"]}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'input_text': input_text, "emotions": emotion_analysis_result}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
            
    # Method that interacts with the (Gemini) API
    def get_emotion_analysis(self, input_text):
        # Add guiding prompt to analyze emotion directly
        modified_input_text = f"{input_text} Analyze the emotional state of the speaker."

        # Perform the OAuth 2.0 flow to get credentials
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=8080)
        # Now you have the OAuth token
        access_token = credentials.token

        # Use the access token in your API request
        api_key = "AIzaSyD46CMD2uVfdLQYTgCHTaqX7A4VSQpadSg"
        api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

        # Payload with modified prompt
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": modified_input_text
                        }
                    ]
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # send request to Gemini API
        response = requests.post(f"{api_endpoint}?key={api_key}", json=payload, headers=headers)
        
        # Handle rsponse and error-check
        if response.status_code == 200:
            result = response.json()
            emotion_text = result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "")
            return emotion_text
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
# # View for Audio Emotion Detection
# class AudioEmotionAnalysisView(APIView):
#     def post(self, request):
#         serializer = AudioEmotionAnalysisSerializer(data=request.data)
#         if serializer.is_valid():
#             audio_file = serializer.validated_data.get('audio_file')
#             # Speech to text (AssemblyAi) API integration
            
#             import assemblyai as aai

#             aai.settings.api_key = "96452f4e5a3e4d2c8f6ac2d7ff6f9485"

#             transcriber = aai.Transcriber()

#             # You can use a local filepath:
#             # audio_file = "./example.mp3"

#             # Or use a publicly-accessible URL:
#             # audio_file = (
#             #     "https://assembly.ai/sports_injuries.mp3"
#             # )

#             config = aai.TranscriptionConfig(speaker_labels=True)

#             transcript = transcriber.transcribe(audio_file, config)

#             if transcript.status == aai.TranscriptStatus.error:
#                 print(f"Transcription failed: {transcript.error}")
#                 exit(1)

#             print(transcript.text)
            
#             # For simplicity, assume it returns the following emotions
#             # emotions = ['angry', 'neutral']  # This should come from AssemblyAI response
            
#             return Response({'audio_file': str(audio_file), 'emotions': transcript.text}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
