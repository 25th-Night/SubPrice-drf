from drf_yasg import openapi
from .serializers import CategorySerializer
from subscriptions.models import Type, Company, Billing, Category, Service, Plan, Subscription


categoryType_list = [category_type[0] for category_type in Category.CATEGORY_TYPE]

categoryList_get = {
    "operation_summary" : "카테고리 목록 조회",
    "operation_id" : '카테고리',
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="카테고리 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="카테고리 정보",
                    properties = {
                        'category_type': openapi.Schema(type=openapi.TYPE_INTEGER, description="카테고리 분류 No.", title="카테고리 종류", enum=categoryType_list),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="카테고리 분류에 따른 이름", title="카테고리 이름", ),
                    }
                )
            )
        ), 
        400: openapi.Response(
            description="Bad Request", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청에 따른 오류 메세지"),
                }
            )
        )
    }
}


serviceId_list = list(Service.objects.all().values_list('id', flat=True))

serviceList_get = {
    "operation_summary" : "서비스 목록 조회",
    "operation_id" : '서비스',
    "manual_parameters" : [
        openapi.Parameter(
            "category",
            openapi.IN_QUERY,
            description="Category Type",
            type=openapi.TYPE_STRING,
            enum=["All"] + categoryType_list,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="서비스 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="서비스 정보",
                    properties = {
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="서비스 분류 No.", title="서비스 종류", enum=serviceId_list),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="서비스 분류에 따른 이름", title="서비스 이름", ),
                    }
                )
            )
        ), 
        400: openapi.Response(
            description="Bad Request", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청에 따른 오류 메세지"),
                }
            )
        )
    }
}