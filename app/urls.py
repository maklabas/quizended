from django.urls import path
from app import views

urlpatterns = [
    path('', views.start, name='start'),
    path('quiz/', views.check, name='quiz'),
    path('results/', views.results, name='results'),
    path('create_question/', views.create_question, name='create_question')]
