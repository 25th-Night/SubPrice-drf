from django.shortcuts import get_object_or_404
from .serializers import SubscriptionSerializer, CategorySerializer
from subscriptions.models import Type, Company, Billing, Category, Service, Plan, Subscription
from alarms.models import Alarm
from users.models import User
from .permissions import IsOwnerOnly
from .paginators import CustomPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from drf_yasg.utils import swagger_auto_schema
from .openapi import categorylist_get


# Create your views here.

class SubscriptionList(APIView):
    permission_classes = [IsOwnerOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        ing = self.request.GET.get('ing', None)

        if ing == "y":
            subscription_list = list(Subscription.objects.select_related('user', 'plan', 'billing', 'alarm_subscription').filter(user=request.user, is_active=1, delete_on=0))
            subscription_list.sort(key=lambda x: x.next_billing_at(), reverse=True)
            page = self.paginate_queryset(subscription_list)
            if page is not None:
                serializered_subscription_data = self.serializer_class(page, many=True).data
                return self.get_paginated_response(serializered_subscription_data)
            serializered_subscription_data = self.serializer_class(subscription_list, many=True).data
            return Response(serializered_subscription_data, status=status.HTTP_200_OK)   

        elif ing == "n":
            subscription_list = Subscription.objects.select_related('user', 'plan', 'billing', 'alarm_subscription').filter(user=request.user, is_active=0, delete_on=0).order_by("-expire_at")[:5]
            serializered_subscription_data = self.serializer_class(subscription_list, many=True).data
            return Response(serializered_subscription_data, status=status.HTTP_200_OK)

    def post(self, request):
        subscription_serializer = self.serializer_class(data=request.data, context={'request': request})
        if subscription_serializer.is_valid():
            subscription_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_201_CREATED)
        return Response(subscription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDetail(APIView):
    permission_classes = [IsOwnerOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubscriptionSerializer

    def get(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk, user=request.user, is_active=1, delete_on=0)
        serializered_subscription_data = self.serializer_class(subscription).data
        return Response(serializered_subscription_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk, user=request.user, is_active=1, delete_on=0)
        self.check_object_permissions(self.request, subscription)
        subscription_serializer = self.serializer_class(subscription, data=request.data, context={'request': request})
        if subscription_serializer.is_valid():
            subscription_serializer.save()
            return Response(subscription_serializer.data, status=status.HTTP_200_OK)
        return Response(subscription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionHistory(APIView):
    permission_classes = [IsOwnerOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        sub_list = Subscription.objects.select_related('user', 'plan', 'billing', 'alarm_subscription').filter(user=request.user, delete_on=0)
        sub_now = list(sub_list.filter(is_active=1))
        sub_now.sort(key=lambda x: x.next_billing_at(), reverse=True)
        sub_exp = list(sub_list.filter(is_active=0).order_by("-expire_at"))
        subscription_list = sub_now + sub_exp
        page = self.paginate_queryset(subscription_list)
        if page is not None:
            serializered_subscription_data = self.serializer_class(page, many=True).data
            return self.get_paginated_response(serializered_subscription_data.data)

        serializered_subscription_data = self.serializer_class(subscription_list, many=True).data
        return Response(serializered_subscription_data, status=status.HTTP_200_OK)

    def put(self, request):
        list_selected = request.data['list_selected']
        
        subscription_list = Subscription.objects.filter(user = request.user, delete_on=False)
        target_subscription = subscription_list.filter(id__in=list_selected)
        target_subscription.update(delete_on=1)
        return Response({"message": "정상"}, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    """
        # 카테고리 목록 조회를 위한 API
        ---
        ## 내용
        
        ### Response body
            - category_id : 
            - category_display : 
    """
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary=categorylist_get["operation_summary"],
        operation_id=categorylist_get["operation_id"],
        responses=categorylist_get["responses"],
    ) 
    def get(self, request):
        category_list = Category.objects.all()
        serialized_category_data = self.serializer_class(category_list, many=True).data
        return Response(serialized_category_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def service_data(request):
    category = request.GET.get('category')
    if category is None:
        service_list = list(Service.objects.all().order_by("id").values_list("id", "name"))
    else:
        service_list = list(Service.objects.filter(category__category_type=category).values_list('id', 'name'))
    return JsonResponse(service_list, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def plan_data(request):
    service = request.GET.get('service')
    if service is None:
        plan_list = list(Plan.objects.all().order_by("id").values_list("id", "name"))
    else:
        plan_list = list(Plan.objects.filter(service=service).values_list('id', 'name'))
    return JsonResponse(plan_list, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def price_data(request):
    plan_id = request.GET.get('plan')
    price = Plan.objects.get(id=plan_id).price
    return JsonResponse(price, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def type_data(request):
    method_type_list = Type.METHOD_TYPE
    return JsonResponse(method_type_list, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def company_data(request):
    method_type = request.GET.get('method_type')
    if method_type is None:
        company_list = list(Company.objects.all().order_by("id").values_list('id', 'company'))
    else:
        CREDIT_CARD, CHECK_CARD, ACCOUNT, EASY_PAYMENT, MOBILE_PAYMENT = 1, 2, 3, 4, 5
        company_type = {CREDIT_CARD:company_list[19:38],CHECK_CARD:company_list[19:37],
                        ACCOUNT:company_list[0:19], EASY_PAYMENT:company_list[38:52], 
                        MOBILE_PAYMENT:company_list[45:46] + company_list[52:57]}
        company_list = company_type[method_type]
    return JsonResponse(company_list, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def dday_data(request):
    d_day_list = Alarm.DDAY_TYPE
    return JsonResponse(d_day_list, safe=False)