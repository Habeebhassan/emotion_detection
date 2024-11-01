from rest_framework import serializers
from .text_model import TextEmotionAnalysis
from .audio_model import AudioEmotionAnalysis

# Serializer for text emotion analysis
class TextEmotionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextEmotionAnalysis
        fields = ['input_text', 'emotion']

# Serializer for audio emotion analysis
class AudioEmotionAnalysisSerializer(serializers.ModelSerializer):
    transcript_text = serializers.CharField(required=False)
    emotion = serializers.CharField(required=False)
    confidence_score = serializers.FloatField(required=False)
    
    class Meta:
        model = AudioEmotionAnalysis
        fields = ['audio_file', 'transcript_text', 'emotion', 'confidence_score', 'analyzed_at']
        