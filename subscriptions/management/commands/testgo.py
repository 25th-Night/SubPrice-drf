import csv
import pandas as pd

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

        # COMPANY_TYPE = Company.objects.all().values_list('id','company')
        # SERVICE_TYPE = Service.objects.all().values_list('id', 'name')
        # PLAN_TYPE = Plan.objects.all().values_list('id', 'name')

        # print(COMPANY_TYPE)
        # print("------")
        # print(SERVICE_TYPE)
        # print("------")
        # print(PLAN_TYPE)

        # company_list = list(Company.objects.all().values_list('id', flat=True))
        # print(company_list)
        # credit_card = company_list[19:38]
        # check_card = company_list[19:37]
        # account = company_list[:19]
        # easy_payment = company_list[38:52]
        # mobile_payment = company_list[45:46] + company_list[52:57]
        # print(credit_card)
        # print(check_card)
        # print(account)
        # print(easy_payment)
        # print(mobile_payment)

        categoryType_list=Category.CATEGORY_TYPE
        print(categoryType_list)
        a = [category_type[0] for category_type in categoryType_list]
        print(a)

        serviceId_list = Service.objects.all().values_list('id', flat=True)
        print(serviceId_list)