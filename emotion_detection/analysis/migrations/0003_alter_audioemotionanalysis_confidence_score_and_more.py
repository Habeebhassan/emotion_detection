# Generated by Django 4.2.16 on 2024-11-01 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_delete_emotioncategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioemotionanalysis',
            name='confidence_score',
            field=models.FloatField(default=0.0, help_text='Confidence level of the emotion prediction.'),
        ),
        migrations.AlterField(
            model_name='audioemotionanalysis',
            name='emotion',
            field=models.CharField(default='unknown', help_text='Predicted emotion label.', max_length=50),
        ),
        migrations.AlterField(
            model_name='audioemotionanalysis',
            name='transcript_text',
            field=models.TextField(default='', help_text='Transcribed text from the audio.'),
        ),
    ]
