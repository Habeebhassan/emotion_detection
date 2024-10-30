from django.db import models

class TextEmotionAnalysis(models.Model):
    """
    Model to store emotion analysis results for text input using Gemini API.

    Fields:
        input_text (str): The text analyzed for emotions.
        emotion (str): Predicted emotion label (e.g., "happy", "sad", etc.).
        confidence_score (float): Confidence level of the emotion prediction.
        analyzed_at (datetime): Timestamp when the analysis was performed.
    """
    input_text = models.TextField(help_text="The text to be analyzed for emotions.")
    emotion = models.CharField(max_length=50, help_text="Predicted emotion label.")
    confidence_score = models.FloatField(help_text="Confidence level of the emotion prediction.")
    analyzed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the analysis.")

    def __str__(self):
        return f"{self.emotion} - {self.confidence_score}"

    class Meta:
        ordering = ['-analyzed_at']
        verbose_name = "Text Emotion Analysis"
        verbose_name_plural = "Text Emotion Analyses"