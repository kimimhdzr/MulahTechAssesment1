from django.urls import path
from .views import headlines_api

urlpatterns = [
    path('headlines/', headlines_api, name='headlines_api'),
]