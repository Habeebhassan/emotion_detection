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
    class Meta:
        model = AudioEmotionAnalysis
        fields = ['audio_file', 'emotion']