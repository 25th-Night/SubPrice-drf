from .serializers import SubscriptionSerializer
from subscriptions.models import Subscription
from .permissions import IsOwnerOnly
from .paginators import CustomPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

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

