from django.db import models

class EmotionCategory(models.Model):
    """
    Model for predefined emotion categories.

    Fields:
        name (str): Name of the emotion category (e.g., "happy", "sad").
        description (str): Detailed description of the emotion.
    """
    name = models.CharField(max_length=50, unique=True, help_text="Name of the emotion category.")
    description = models.TextField(help_text="Description of the emotion.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Emotion Category"
        verbose_name_plural = "Emotion Categories"