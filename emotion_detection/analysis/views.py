from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import AutoTokenizer, AutoModel
import torch  # Required for tensor operations
from .serializers import TextEmotionAnalysisSerializer, AudioEmotionAnalysisSerializer
import assemblyai as aai
import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Retrieve the Hugging Face token from the environment
hf_token = os.getenv("HUGGINGFACE_TOKEN")

# Set up AssemblyAI API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Initialize the tokenizer and model for Mental-BERT
tokenizer = AutoTokenizer.from_pretrained("mental/mental-bert-base-uncased", use_auth_token=hf_token)
model = AutoModel.from_pretrained("mental/mental-bert-base-uncased", use_auth_token=hf_token)

# Define labels based on model's intended classifications
LABELS = {
    0: "No Depression", 1: "Depression",
    2: "No Suicide", 3: "Suicide",
    4: "No Distress", 5: "Distress"
}

class TextEmotionAnalysisView(APIView):
    """
    API view for analyzing the mental health status of text input using Mental-BERT.
    """

    def post(self, request):
        """
        Handle POST requests to analyze text for mental health conditions like Depression, Suicide, and Distress.
        """
        from .text_model import TextEmotionAnalysis
        
        logger.info("POST request received at /api/analyze-text/")  # Log the start of the request
        serializer = TextEmotionAnalysisSerializer(data=request.data)
        
        if serializer.is_valid():
            input_text = serializer.validated_data.get('input_text')
            emotion_analysis_result = self.analyze_emotion(input_text)

             # Log the emotion analysis result before returning
            logger.info(f"Emotion analysis result: {emotion_analysis_result}")


            if "error" in emotion_analysis_result:
                return Response({"error": emotion_analysis_result["error"]}, status=status.HTTP_400_BAD_REQUEST)


            # Log the successful result being returned
            logger.info(f"Returning analysis result: {emotion_analysis_result}")


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

        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def analyze_emotion(self, input_text):
        """
        Analyze the mental health content of the input text using Mental-BERT.
        """
        try:
            # Tokenize and encode the input text
            inputs = tokenizer(input_text, return_tensors="pt")
            outputs = model(**inputs)

            # Assuming the model outputs logits for classification, apply softmax for probabilities
            logits = outputs.last_hidden_state[:, 0, :]  # Use CLS token representation
            probs = torch.softmax(logits, dim=1)
            max_prob, max_index = torch.max(probs, dim=1)

            # Get the predicted emotion label and confidence score
            predicted_label = max_index.item()
            confidence_score = max_prob.item()

            # Map the label to a more readable form
            emotion = LABELS.get(predicted_label, "Unknown")
            
            return {'emotion': emotion, 'confidence_score': confidence_score}

        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            return {"error": str(e)}

class AudioEmotionAnalysisView(APIView):
    """
    API view for analyzing mental health status from an audio input.
    """

    def post(self, request, *args, **kwargs):
        serializer = AudioEmotionAnalysisSerializer(data=request.data)
        
        if serializer.is_valid():
            audio_file = request.FILES['audio_file']
            
            # Save the audio file to initiate transcription and analysis
            instance = serializer.save()

            # Transcribe the audio using AssemblyAI
            transcription_result = self.transcribe_audio(instance.audio_file.path)

            if "error" in transcription_result:
                return Response({"error": transcription_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Analyze the transcription for mental health status
            emotion_analysis_result = self.analyze_emotion(transcription_result['transcript_text'])

            if "error" in emotion_analysis_result:
                return Response({"error": emotion_analysis_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Save results to the database
            instance.transcript_text = transcription_result['transcript_text']
            instance.emotion = emotion_analysis_result['emotion']
            instance.confidence_score = emotion_analysis_result['confidence_score']
            instance.save()

            return Response(AudioEmotionAnalysisSerializer(instance).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes the audio file at the specified path using AssemblyAI.
        """
        try:
            transcriber = aai.Transcriber()
            config = aai.TranscriptionConfig(speaker_labels=True)

            # Attempt transcription of the audio file
            transcript = transcriber.transcribe(audio_file_path, config)

            if transcript.status == aai.TranscriptStatus.error:
                return {"error": f"Transcription failed: {transcript.error}"}

            speaker_labels = getattr(transcript, "speaker_labels", [])
            return {
                'transcript_text': transcript.text,
                'speaker_labels': speaker_labels
            }
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return {"error": f"An error occurred during transcription: {str(e)}"}

    def analyze_emotion(self, text):
        """
        Analyze the mental health content of the transcribed text using Mental-BERT.
        """
        try:
            # Tokenize and encode the text
            inputs = tokenizer(text, return_tensors="pt")
            outputs = model(**inputs)

            # Use logits for classification and softmax for probabilities
            logits = outputs.last_hidden_state[:, 0, :]
            probs = torch.softmax(logits, dim=1)
            max_prob, max_index = torch.max(probs, dim=1)

            # Map the predicted label and return with confidence score
            predicted_label = max_index.item()
            confidence_score = max_prob.item()
            emotion = LABELS.get(predicted_label, "Unknown")
            
            return {'emotion': emotion, 'confidence_score': confidence_score}
        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            return {"error": str(e)}