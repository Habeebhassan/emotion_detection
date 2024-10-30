from django.urls import path
from .views import TextEmotionAnalysisView, AudioEmotionAnalysisView

urlpatterns = [
    path('analyze-text/', TextEmotionAnalysisView.as_view(), name='analyze-text'),
    path('analyze-audio/', AudioEmotionAnalysisView.as_view(), name='analyze-audio'),
]