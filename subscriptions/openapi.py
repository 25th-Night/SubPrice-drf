from drf_yasg import openapi
from .serializers import CategorySerializer


category_data_get = {
    "method" : "get",
    "operation_summary" : "카테고리 목록 조회",
    "operation_id" : '카테고리',
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                descriptio="카테고리 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="카테고리 정보",
                    properties = {
                        'category_type': openapi.Schema(type=openapi.TYPE_INTEGER, description="카테고리 분류 No.", title="카테고리 종류", enum=list(range(1,8))),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="카테고리 분류에 따른 이름", title="카테고리 이름", ),
                    }
                )
            )
        ), 
        # 200 : CategorySerializer,
        400: openapi.Response(
            description="Not found or Not accessible", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청에 따른 오류 메세지"),
                }
            )
        )
    }
}
