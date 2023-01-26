from django.urls import path
from users.views import LoginView, SignUpView, MyInfoView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("myinfo/", MyInfoView.as_view(), name="myinfo"),
]