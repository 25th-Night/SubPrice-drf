from django.urls import path
from subscriptions.views import SubscriptionList, SubscriptionDetail, SubscriptionHistory, CategoryListView, ServiceListView, PlanListView, priceData, TypeListView, CompanyListView, AlarmListView

urlpatterns = [
    path("main/", SubscriptionList.as_view(), name="subscription_list"),
    path("main/<int:pk>/", SubscriptionDetail.as_view(), name="subscription_detail"),
    path("history/", SubscriptionHistory.as_view(), name="subscription_history"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("service/", ServiceListView.as_view(), name="service_list"),
    path("plan/", PlanListView.as_view(), name="plan_list"),
    path("price/", priceData, name="price_list"),
    path("method_type/", TypeListView.as_view(), name="method_type_list"),
    path("company/", CompanyListView.as_view(), name="company_list"),
    path("dday/", AlarmListView.as_view(), name="dday_list"),
]