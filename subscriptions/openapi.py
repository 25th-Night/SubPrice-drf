from drf_yasg import openapi

from subscriptions.serializers import SubscriptionSerializer
from subscriptions.models import Type, Company, Billing, Category, Service, Plan, Subscription
from alarms.models import Alarm

import csv
import pandas as pd
import boto3
import io

from django.conf import settings


target_list = ["company.csv", "service.csv", "plan.csv"]
data_list = []

if settings.CSV_READ_FROM == 'here':
    
    BASE_DIR = './static/csv/'
    
    csv_list = []

    for target in target_list:
        csv_path = BASE_DIR + target
        csv_list.append(csv_path)

    for csv_file in csv_list:
        with open(csv_file, 'rt', encoding='UTF8') as f:
            dr = csv.DictReader(f)
            data_list.append(pd.DataFrame(dr))

elif settings.CSV_READ_FROM == 's3':

    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    region_name = settings.AWS_REGION

    s3_client = boto3.client(service_name="s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    for i in range(3):
        obj = s3_client.get_object(Bucket="subprice", Key="static/csv/" + target_list[i])
        data_list.append(pd.read_csv(io.BytesIO(obj["Body"].read())))

company_data, service_data, plan_data = data_list[0], data_list[1], data_list[2]



categoryType_list = [category_type[0] for category_type in Category.CATEGORY_TYPE]
serviceId_list = list(map(int,service_data[service_data.columns[0]]))
planId_list = plan_data[plan_data.columns[0]].to_list()
methodType_list = [method_type[0] for method_type in Type.METHOD_TYPE]
companyId_list = company_data[company_data.columns[0]].to_list()
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
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
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
            type=openapi.TYPE_INTEGER,
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
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
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
            type=openapi.TYPE_INTEGER,
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
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
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
            type=openapi.TYPE_INTEGER,
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
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
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
            type=openapi.TYPE_INTEGER,
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
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
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
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
                }
            )
        )
    }
}


subscriptionList_get = {
    "operation_summary" : "구독정보 목록 조회",
    "operation_id" : '구독정보',
    "manual_parameters" : [
        openapi.Parameter(
            "ing",
            openapi.IN_QUERY,
            description="**현재 구독 여부** <br> \
                        - `y` 입력 : 구독 중인 서비스 조회  <br>\
                        - `n` 입력 : 구독 만료된 서비스 조회 ",
            type=openapi.TYPE_STRING,
            enum=["y","n"],
            required=True,
        ),
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            description="**표시할 페이지 No.**",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=SubscriptionSerializer(many=True),
        ),
        404: openapi.Response(
            description="Not Found", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="찾을 수 없습니다."),
                }
            )
        )
    }
}


subscriptionDetail_get = {
    "operation_summary" : "구독정보 조회",
    "operation_id" : '단일 구독정보',
    "manual_parameters" : [
        openapi.Parameter(
            "page",
            openapi.IN_PATH,
            description="**구독정보 ID**",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=SubscriptionSerializer,
        ),
        400: openapi.Response(
            description="Bad Request", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
                }
            )
        )
    }
}


historyList_get = {
    "operation_summary" : "구독내역 목록 조회",
    "operation_id" : '구독내역',
    "manual_parameters" : [
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            description="**표시할 페이지 No.**",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=SubscriptionSerializer(many=True),
        ),
        400: openapi.Response(
            description="Bad Request", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
                }
            )
        )
    }
}