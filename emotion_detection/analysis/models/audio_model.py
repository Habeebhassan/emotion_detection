from django.db import models

class AudioEmotionAnalysis(models.Model):
    """
    Model to store emotion analysis results for audio input using AssemblyAI API.

    Fields:
        audio_file_url (str): URL or path to the audio file.
        transcript_text (str): Transcribed text from the audio.
        emotion (str): Predicted emotion label (e.g., "angry", "calm").
        confidence_score (float): Confidence level of the emotion prediction.
        analyzed_at (datetime): Timestamp of when the audio was analyzed.
    """
    audio_file_url = models.URLField(help_text="URL of the audio file for analysis.")
    transcript_text = models.TextField(help_text="Transcribed text from the audio.")
    emotion = models.CharField(max_length=50, help_text="Predicted emotion label.")
    confidence_score = models.FloatField(help_text="Confidence level of the emotion prediction.")
    analyzed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the analysis.")

    def __str__(self):
        return f"{self.emotion} - {self.confidence_score}"

    class Meta:
        ordering = ['-analyzed_at']
        verbose_name = "Audio Emotion Analysis"
        verbose_name_plural = "Audio Emotion Analyses"