from django.urls import include, path

from ai_api.views import Predict_Image

urlpatterns = [
    path('detect/', Predict_Image.as_view())
]