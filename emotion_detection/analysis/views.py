from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextEmotionAnalysisSerializer, AudioEmotionAnalysisSerializer

import requests
import os
import assemblyai as aai
from google_auth_oauthlib.flow import InstalledAppFlow
import logging

logger = logging.getLogger(__name__)
# Path to your downloaded OAuth credentials file
CLIENT_SECRETS_FILE = "../../../client_secret_393908793020-tahceb69n7oigbhks4havcjciguec1m0.apps.googleusercontent.com.json"
# Scopes required for the Generative Language API
SCOPES = [
    "https://www.googleapis.com/auth/generative-language.tuning",
    "https://www.googleapis.com/auth/cloud-platform"
]

# Set up AssemblyAI API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")  # Ensure you have your API key in your environment variables

# View for Text Emotion Detection
class TextEmotionAnalysisView(APIView):
    """
    API view for analyzing the emotional content of text input using the Gemini API.
    """

    def post(self, request):
        """
        Handle POST requests to analyze text emotions.

        Validates incoming data, processes the text through the Gemini API,
        and saves the detected emotions in the database.

        Args:
            request (Request): The incoming HTTP request containing text data.

        Returns:
            Response: A JSON response containing the input text and the detected emotions,
                      or an error message if validation fails or if there are issues with the analysis.
        """
        from .text_model import TextEmotionAnalysis
        serializer = TextEmotionAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data.get('input_text')
            emotion_analysis_result = self.analyze_emotion(input_text)

            if "error" in emotion_analysis_result:
                return Response({"error": emotion_analysis_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Save the analysis result to the database
            analysis_record = TextEmotionAnalysis(
                input_text=input_text,
                emotion=emotion_analysis_result['emotion'],
                confidence_score=emotion_analysis_result['confidence_score']
            )
            analysis_record.save()

            return Response({
                'input_text': input_text,
                'predicted_emotion': emotion_analysis_result['emotion'],
                'confidence_score': emotion_analysis_result['confidence_score']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def analyze_emotion(self, input_text):
        """
        Interact with the Gemini API to analyze emotions in the given text.

        Args:
            input_text (str): The text input to be analyzed for emotional content.

        Returns:
            dict: A dictionary containing the predicted emotion and confidence score, or an error message if the API call fails.
        """
        # Perform the OAuth 2.0 flow to get credentials
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=8080)
        access_token = credentials.token

        # Define the Gemini API endpoint and headers
        api_key = "AIzaSyD46CMD2uVfdLQYTgCHTaqX7A4VSQpadSg"
        api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

        # Prepare the prompt for emotion analysis
        modified_input_text = f"{input_text} Analyze the emotional state of the speaker."

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

        # Send request to Gemini API
        response = requests.post(f"{api_endpoint}?key={api_key}", json=payload, headers=headers)

        # Handle response and extract emotion
        if response.status_code == 200:
            result = response.json()
            emotion_text = result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "unknown")
            confidence_score = 0.95  # Replace with actual confidence score if available
            return {'emotion': emotion_text, 'confidence_score': confidence_score}
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}


# View for Audio Emotion Detection
class AudioEmotionAnalysisView(APIView):
    """
    API view for analyzing the emotional content of audio input by transcribing speech to text
    and predicting the emotion of the speaker using the Gemini API.
    """

    def post(self, request):
        """
        Handle POST requests to analyze audio emotions.

        Validates incoming data, transcribes the audio using the AssemblyAI API,
        and predicts the emotional state of the speaker based on the transcription,
        saving the results to the database.

        Args:
            request (Request): The incoming HTTP request containing the audio file.

        Returns:
            Response: A JSON response containing the audio file, the transcribed text,
                      and predicted emotions, or an error message if validation fails
                      or if transcription fails.
        """
        from .audio_model import AudioEmotionAnalysis as AudioAnalysisModel
        serializer = AudioEmotionAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data.get('audio_file')

            # Use AssemblyAI to transcribe the audio
            transcription_result = self.transcribe_audio(audio_file)

            if "error" in transcription_result:
                return Response({"error": transcription_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Use the transcribed text to analyze emotion
            emotion_analysis_result = self.analyze_emotion(transcription_result['transcript_text'])

            if "error" in emotion_analysis_result:
                return Response({"error": emotion_analysis_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Save the analysis result to the database
            analysis_record = AudioAnalysisModel(
                audio_file_url=str(audio_file),
                transcript_text=transcription_result['transcript_text'],
                emotion=emotion_analysis_result['emotion'],
                confidence_score=emotion_analysis_result['confidence_score']
            )
            analysis_record.save()

            return Response({
                'audio_file': str(audio_file),
                'transcription': transcription_result['transcript_text'],
                'predicted_emotion': emotion_analysis_result['emotion'],
                'confidence_score': emotion_analysis_result['confidence_score']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def transcribe_audio(self, audio_file):
        """
        Transcribe the audio file using AssemblyAI.

        Args:
            audio_file (File): The audio file to be transcribed.

        Returns:
            dict: A dictionary containing the transcribed text or an error message if transcription fails.
        """
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(speaker_labels=True)

        # Transcribe the audio file
        transcript = transcriber.transcribe(audio_file, config)

        if transcript.status == aai.TranscriptStatus.error:
            return {"error": f"Transcription failed: {transcript.error}"}

        return {
            'transcript_text': transcript.text,
            'speaker_labels': transcript.speaker_labels
        }

    def analyze_emotion(self, text):
        """
        Analyze the emotional state of the speaker based on transcribed text using the Gemini API.

        Args:
            text (str): The transcribed text to analyze.

        Returns:
            dict: A dictionary containing the predicted emotion and confidence score, or an error message if the API call fails.
        """
        # Perform the OAuth 2.0 flow to get credentials
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=8080)
        access_token = credentials.token

        # Define the Gemini API endpoint and headers
        api_key = "AIzaSyD46CMD2uVfdLQYTgCHTaqX7A4VSQpadSg"
        api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

        # Prepare the prompt for emotion analysis
        modified_input_text = f"{text} Analyze the emotional state of the speaker."

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

        # Send request to Gemini API
        response = requests.post(f"{api_endpoint}?key={api_key}", json=payload, headers=headers)

        # Handle response and extract emotion
        if response.status_code == 200:
            result = response.json()
            emotion_text = result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "unknown")
            confidence_score = result.get("confidence_score", 0.95)  # Replace with actual confidence score if available
            return {'emotion': emotion_text, 'confidence_score': confidence_score}
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import TextEmotionAnalysisSerializer, AudioEmotionAnalysisSerializer
# from .text_model import TextEmotionAnalysis
# from .audio_model import AudioEmotionAnalysis
# import assemblyai as aai
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# import requests
# import json
# import os

# # Path to your downloaded OAuth credentials file
# CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")
# # Scopes required for the Generative Language API
# SCOPES = ["https://www.googleapis.com/auth/generative-language.tuning", "https://www.googleapis.com/auth/cloud-platform"]

# # View for Text Emotion Detection
# class TextEmotionAnalysisView(APIView):
#     """
#     API view for analyzing the emotional content of text input.

#     This view accepts a POST request with text data and returns the detected emotions 
#     using a generative language model.
#     """

#     def post(self, request):
#         """
#         Handle POST requests to analyze text emotions.

#         Validates incoming data, processes the text through the emotion analysis model,
#         and returns the result or an error message.

#         Args:
#             request (Request): The incoming HTTP request containing text data.

#         Returns:
#             Response: A JSON response containing the input text and the detected emotions,
#                       or an error message if validation fails or if there are issues with the analysis.
#         """
#         serializer = TextEmotionAnalysisSerializer(data=request.data)
#         if serializer.is_valid():
#             # Process the text input using Gemini API
#             input_text = serializer.validated_data.get('input_text')
#             emotion_analysis_result = self.get_emotion_analysis(input_text)

#             if "error" in emotion_analysis_result:
#                 return Response({"error": emotion_analysis_result["error"]}, status=status.HTTP_400_BAD_REQUEST)
            
#             return Response({'input_text': input_text, "emotions": emotion_analysis_result}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_emotion_analysis(self, input_text):
#         """
#         Interact with the Gemini API to analyze emotions in the given text.

#         Prepares the input text with a specific prompt, performs OAuth 2.0 authentication,
#         and sends the request to the Gemini API to retrieve emotion analysis.

#         Args:
#             input_text (str): The text input to be analyzed for emotional content.

#         Returns:
#             dict: The result of the emotion analysis, or an error message if the API call fails.
#         """
#         # Add guiding prompt to analyze emotion directly
#         modified_input_text = f"{input_text} Analyze the emotional state of the speaker."

#         # Perform the OAuth 2.0 flow to get credentials
#         flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#         credentials = flow.run_local_server(port=8080)
#         # Now you have the OAuth token
#         access_token = credentials.token

#         # Use the access token in your API request
#         api_key = "AIzaSyD46CMD2uVfdLQYTgCHTaqX7A4VSQpadSg"
#         api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

#         # Payload with modified prompt
#         payload = {
#             "contents": [
#                 {
#                     "parts": [
#                         {
#                             "text": modified_input_text
#                         }
#                     ]
#                 }
#             ]
#         }

#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json"
#         }

#         # Send request to Gemini API
#         response = requests.post(f"{api_endpoint}?key={api_key}", json=payload, headers=headers)
        
#         # Handle response and error-check
#         if response.status_code == 200:
#             result = response.json()
#             emotion_text = result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "")
#             return emotion_text
#         else:
#             return {"error": f"Error {response.status_code}: {response.text}"}

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
