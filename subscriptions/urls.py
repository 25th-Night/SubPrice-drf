from django.urls import path
from subscriptions.views import SubscriptionList, SubscriptionDetail

urlpatterns = [
    path("main/", SubscriptionList.as_view(), name="subscription_list"),
    path("main/<int:pk>/", SubscriptionDetail.as_view(), name="subscription_detail"),

]