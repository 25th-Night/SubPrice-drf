from django.urls import path
from subscriptions.views import SubscriptionList, SubscriptionDetail, SubscriptionHistory, CategoryListView, ServiceListView, PlanListView, price_data, type_data, company_data, dday_data

urlpatterns = [
    path("main/", SubscriptionList.as_view(), name="subscription_list"),
    path("main/<int:pk>/", SubscriptionDetail.as_view(), name="subscription_detail"),
    path("history/", SubscriptionHistory.as_view(), name="subscription_history"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("service/", ServiceListView.as_view(), name="service_list"),
    path("plan/", PlanListView.as_view(), name="plan_list"),
    path("price/", price_data, name="price_list"),
    path("method_type/", type_data, name="method_type_list"),
    path("company/", company_data, name="company_list"),
    path("dday/", dday_data, name="dday_list"),
]