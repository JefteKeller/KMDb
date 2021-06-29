from django.urls import path

from .views import CreateUserView, LoginView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('accounts/', CreateUserView.as_view()),
]
