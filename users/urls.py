from django.urls import path
from users.views import LoginView, MyInfoView


urlpatterns = [
    path("login/", LoginView.as_view()),
    path("mypage/", MyInfoView.as_view()),
]