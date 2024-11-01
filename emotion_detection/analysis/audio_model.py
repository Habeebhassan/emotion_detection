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
    audio_file = models.FileField(upload_to='audio_files/', help_text='Uploaded audio file for analysis.')
    transcript_text = models.TextField(help_text="Transcribed text from the audio.", default="")
    emotion = models.CharField(max_length=50, help_text="Predicted emotion label.", default="unknown")
    confidence_score = models.FloatField(help_text="Confidence level of the emotion prediction.", default=0.0)
    analyzed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the analysis.")

    def __str__(self):
        return f"{self.emotion} - {self.confidence_score}"

    class Meta:
        ordering = ['-analyzed_at']
        verbose_name = "Audio Emotion Analysis"
        verbose_name_plural = "Audio Emotion Analyses"