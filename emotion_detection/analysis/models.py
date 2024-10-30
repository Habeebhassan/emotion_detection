# from django.db import models

# class TextEmotionAnalysis(models.Model):
#     """
#     Model to store emotion analysis results for text input using Gemini API.

#     Fields:
#         input_text (str): The text analyzed for emotions.
#         emotion (str): Predicted emotion label (e.g., "happy", "sad", etc.).
#         confidence_score (float): Confidence level of the emotion prediction.
#         analyzed_at (datetime): Timestamp when the analysis was performed.
#     """
#     input_text = models.TextField(help_text="The text to be analyzed for emotions.")
#     emotion = models.CharField(max_length=50, help_text="Predicted emotion label.")
#     confidence_score = models.FloatField(help_text="Confidence level of the emotion prediction.")
#     analyzed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the analysis.")

#     def __str__(self):
#         return f"{self.emotion} - {self.confidence_score}"

#     class Meta:
#         ordering = ['-analyzed_at']
#         verbose_name = "Text Emotion Analysis"
#         verbose_name_plural = "Text Emotion Analyses"
  
        
# class AudioEmotionAnalysis(models.Model):
#     """
#     Model to store emotion analysis results for audio input using AssemblyAI API.

#     Fields:
#         audio_file_url (str): URL or path to the audio file.
#         transcript_text (str): Transcribed text from the audio.
#         emotion (str): Predicted emotion label (e.g., "angry", "calm").
#         confidence_score (float): Confidence level of the emotion prediction.
#         analyzed_at (datetime): Timestamp of when the audio was analyzed.
#     """
#     audio_file_url = models.URLField(help_text="URL of the audio file for analysis.")
#     transcript_text = models.TextField(help_text="Transcribed text from the audio.")
#     emotion = models.CharField(max_length=50, help_text="Predicted emotion label.")
#     confidence_score = models.FloatField(help_text="Confidence level of the emotion prediction.")
#     analyzed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the analysis.")

#     def __str__(self):
#         return f"{self.emotion} - {self.confidence_score}"

#     class Meta:
#         ordering = ['-analyzed_at']
#         verbose_name = "Audio Emotion Analysis"
#         verbose_name_plural = "Audio Emotion Analyses"
        
        
# class EmotionCategory(models.Model):
#     """
#     Model for predefined emotion categories.

#     Fields:
#         name (str): Name of the emotion category (e.g., "happy", "sad").
#         description (str): Detailed description of the emotion.
#     """
#     name = models.CharField(max_length=50, unique=True, help_text="Name of the emotion category.")
#     description = models.TextField(help_text="Description of the emotion.")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Emotion Category"
#         verbose_name_plural = "Emotion Categories"