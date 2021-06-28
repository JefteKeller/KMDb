from django.urls import path
from .views import (
    ListCreateMovieView,
    RetrieveDeleteMovieView,
    CreateUpdateReviewView,
    CreateUpdateCommentView,
)

urlpatterns = [
    path('movies/', ListCreateMovieView.as_view()),
    path('movies/<int:pk>/', RetrieveDeleteMovieView.as_view()),
    path('movies/<int:pk>/review/', CreateUpdateReviewView.as_view()),
    path('movies/<int:pk>/comments/', CreateUpdateCommentView.as_view()),
]
