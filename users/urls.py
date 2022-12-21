from django.urls import path
from users.views import LoginView, SignUpView, MyInfoView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("mypage/", MyInfoView.as_view()),
]