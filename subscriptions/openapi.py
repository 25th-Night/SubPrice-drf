from drf_yasg import openapi
from subscriptions.serializers import CategorySerializer
from subscriptions.models import Type, Company, Billing, Category, Service, Plan, Subscription
from alarms.models import Alarm


categoryType_list = [category_type[0] for category_type in Category.CATEGORY_TYPE]
serviceId_list = list(Service.objects.all().values_list('id', flat=True))
planId_list = list(Plan.objects.all().values_list('id', flat=True))
methodType_list = [method_type[0] for method_type in Type.METHOD_TYPE]
companyId_list = list(Company.objects.all().values_list('id', flat=True))
ddayType_list = [dday_type[0] for dday_type in Alarm.DDAY_TYPE]


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


serviceList_get = {
    "operation_summary" : "서비스 목록 조회",
    "operation_id" : '서비스',
    "manual_parameters" : [
        openapi.Parameter(
            "category",
            openapi.IN_QUERY,
            description="**Category Type** : 카테고리 Type 입력. 미입력 시, 전체 서비스 리스트 조회.  <br>\
                        - 참고 : [Category(카테고리) 목록](https://docs.google.com/spreadsheets/d/1MYBc6fn0Xbw7vbK2jpcBYu02jukmI-8emvralamyyW8/edit#gid=0?usp=share_link) ",
            type=openapi.TYPE_NUMBER,
            enum=categoryType_list,
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
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="서비스 분류 ID", title="서비스 ID", enum=serviceId_list),
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


planList_get = {
    "operation_summary" : "서비스유형 목록 조회",
    "operation_id" : '서비스유형',
    "manual_parameters" : [
        openapi.Parameter(
            "service",
            openapi.IN_QUERY,
            description="**Service Id** : 서비스 ID 입력. 미입력 시, 전체 서비스유형 리스트 조회.  <br>\
                        - 참고 : [Service(서비스) 목록](https://docs.google.com/spreadsheets/d/1MYBc6fn0Xbw7vbK2jpcBYu02jukmI-8emvralamyyW8/edit#gid=32248500?usp=share_link) ",
            type=openapi.TYPE_NUMBER,
            enum=serviceId_list,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="서비스유형 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="서비스유형 정보",
                    properties = {
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="서비스유형 분류 ID", title="서비스유형 ID", enum=planId_list),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="서비스유형 분류에 따른 이름", title="서비스유형 이름", ),
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


price_get = {
    "operation_summary" : "서비스유형 구독료 조회",
    "operation_id" : '서비스유형 구독료',
    "manual_parameters" : [
        openapi.Parameter(
            "plan",
            openapi.IN_QUERY,
            description="**Plan Id** : 서비스유형 ID 입력. 해당 데이터 필수 입력 요망,  <br>\
                        - 참고 : [Plan(서비스유형) 목록](https://docs.google.com/spreadsheets/d/1MYBc6fn0Xbw7vbK2jpcBYu02jukmI-8emvralamyyW8/edit#gid=1831498595?usp=share_link) ",
            type=openapi.TYPE_NUMBER,
            enum=planId_list,
            required=True,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'price': openapi.Schema(type=openapi.TYPE_INTEGER, description="서비스유형에 따른 월 구독료", title="서비스유형 구독료"),
                }
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


typeList_get = {
    "operation_summary" : "결제유형 목록 조회",
    "operation_id" : '결제유형',
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="결제유형 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="결제유형 정보",
                    properties = {
                        'method_type': openapi.Schema(type=openapi.TYPE_INTEGER, description="결제유형 분류 No.", title="결제유형 종류", enum=methodType_list),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="결제유형 분류에 따른 이름", title="결제유형 이름", ),
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


companyList_get = {
    "operation_summary" : "결제사 목록 조회",
    "operation_id" : '결제사',
    "manual_parameters" : [
        openapi.Parameter(
            "method_type",
            openapi.IN_QUERY,
            description="**Method Type** : 결제유형 입력. 미입력 시, 전체 결제사 리스트 조회.  <br>\
                        - 참고 : [Type(결제유형) 목록](https://docs.google.com/spreadsheets/d/1MYBc6fn0Xbw7vbK2jpcBYu02jukmI-8emvralamyyW8/edit#gid=135446740?usp=share_link) ",
            type=openapi.TYPE_NUMBER,
            enum=methodType_list,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="결제사 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="결제사 정보",
                    properties = {
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="결제사 분류 ID", title="결제사 ID", enum=companyId_list),
                        'company': openapi.Schema(type=openapi.TYPE_STRING, description="결제사 분류에 따른 이름", title="결제사 이름", ),
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


ddayList_get = {
    "operation_summary" : "메일발송 D-DAY 목록 조회",
    "operation_id" : '메일발송 D-DAY',
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="메일발송 D-DAY 리스트",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="메일발송 D-DAY 정보",
                    properties = {
                        'd_day': openapi.Schema(type=openapi.TYPE_INTEGER, description="메일발송 D-DAY 분류 No.", title="메일발송 D-DAY 종류", enum=ddayType_list),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="메일발송 D-DAY 분류에 따른 이름", title="메일발송 D-DAY 명칭", ),
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