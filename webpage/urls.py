from django.urls import path
from . import views

urlpatterns = [
    path('webpage/', views.show_images, name = 'show_images')
]