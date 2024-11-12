from rest_framework import serializers
from .text_model import TextEmotionAnalysis
from .audio_model import AudioEmotionAnalysis

# Serializer for text emotion analysis
class TextEmotionAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for handling text-based emotion analysis data.

    Maps fields from the TextEmotionAnalysis model to JSON format
    for API responses and requests.

    Fields:
        input_text (str): The input text to be analyzed for emotions.
        emotion (str): The predicted emotion from the input text.
    """

    emotion = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = TextEmotionAnalysis
        fields = ['input_text', 'emotion']


# Serializer for audio emotion analysis
class AudioEmotionAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for handling audio-based emotion analysis data.

    Maps fields from the AudioEmotionAnalysis model to JSON format
    for API responses and requests, including optional fields for
    the transcription and emotion prediction details.

    Fields:
        audio_file (File): The audio file uploaded for emotion analysis.
        transcript_text (str, optional): The transcribed text from the audio.
        emotion (str, optional): The predicted emotion derived from the audio.
        confidence_score (float, optional): The confidence score of the predicted emotion.
        analyzed_at (datetime): Timestamp of when the analysis was performed.
    """
    transcript_text = serializers.CharField(required=False)
    emotion = serializers.CharField(required=False)
    confidence_score = serializers.FloatField(required=False)
    
    class Meta:
        model = AudioEmotionAnalysis
        fields = ['audio_file', 'transcript_text', 'emotion', 'confidence_score', 'analyzed_at']
