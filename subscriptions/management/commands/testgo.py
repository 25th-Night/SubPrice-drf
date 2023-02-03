import csv
import pandas as pd
import boto3
import io

from django.conf import settings

from users.models import User
from alarms.models import Alarm
from subscriptions.models import Type, Company, Billing, Category, Service, Plan, Subscription
from django.core.management.base import BaseCommand

# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "PUSH CSV DB"

    # test 목적의 파일
    # 아래에 코드를 작성하여 터미널 창에 'python manage.py testgo' 입력하여 실행 결과 확인
    def handle(self, *args, **options):


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

        # company_data, service_data, plan_data = data_list[0], data_list[1], data_list[2]
        
        company_data= data_list[0]
        service_data = data_list[1]
        plan_data = data_list[2]
            

        # serviceId_list = list(service_data.index)
        # print(serviceId_list)
        # serviceId_list = service_data[['id']]
        # print(serviceId_list)
        
        print(service_data)
        print(service_data.columns)
        print(service_data.columns[0])
        print(service_data[service_data.columns[0]].values.tolist())
        print(service_data[service_data.columns[0]].values)
        print(type(service_data[service_data.columns[0]].values.tolist()))
        print(type(service_data[service_data.columns[0]].values))
        print(list(map(int, service_data[service_data.columns[0]].values)))
        print("id" == service_data.columns[0])
        print(f'id:{type("id")}')
        print(f'{service_data.columns[0]}:{type(service_data.columns[0])}')
        print(type(service_data))
        
        # serviceId_list = list(map(int, service_data[service_data.columns[0]].values))
        # planId_list = list(map(int, plan_data[plan_data.columns[0]].values))
        # companyId_list = list(map(int, company_data[company_data.columns[0]].values))
        
        # print(serviceId_list)
        # print(planId_list)
        # print(companyId_list)
        
        
        print('------------')
        
        service_list = service_data[service_data.columns[0]].values
        print(service_list)
        print(type(service_list))
        service_list=service_list.astype(int)
        print(service_list)
        print(service_list[10])
        service_list = list(service_list)
        print(service_list)
        
        service_list = service_data[service_data.columns[0]].values.astype(int)
        print(service_list)
        
        print('------------')
        
        
        service_list = service_data[service_data.columns[0]].to_list()
        print(service_list)
        
        service_list = service_data[service_data.columns[0]].values.tolist()
        print(service_list)
        
        service_list = list(map(int, service_list))
        print(service_list)
        
        
        service_list = list(map(int,service_data[service_data.columns[0]]))
        print(service_list)
        print(type(service_list))
        
        service_list = service_data[service_data.columns[0]]
        service_list = service_list.astype(int)
        service_list = list(service_list)
        print(service_list)
        print(type(service_list))