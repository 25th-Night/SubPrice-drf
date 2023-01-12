from django.urls import path
from subscriptions.views import SubscriptionList

urlpatterns = [
    path("main/", SubscriptionList.as_view(), name="subscription_list"),

]