from rest_framework import serializers

from alarms.models import Alarm
from subscriptions.models import Type, Company, Billing, Category, Service, Plan, Subscription
from alarms.serializers import AlarmSerializer

import calendar
from datetime import datetime

class TypeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.get_method_type_display()
        return name
    class Meta:
        model = Type
        fields = ['method_type', 'name']

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    class Meta:
        model = Company
        fields = ['id', 'company']
        read_only_fields = ['company']

class BillingSerializer(serializers.ModelSerializer):
    type = TypeSerializer(required=True)
    company = CompanySerializer(required=True)

    class Meta:
        model = Billing
        fields = ['id', 'type', 'company']

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.get_category_type_display()
        return name

    class Meta:
        model = Category
        fields = ['category_type', 'name']

class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    category = CategorySerializer(required=True, write_only=True)

    class Meta:
        model = Service
        fields = ['id', 'category', 'name']
        read_only_fields = ['name']

class PlanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    service = ServiceSerializer(required=True, write_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'service', 'name']
        read_only_fields = ['name']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(required=True)
    billing = BillingSerializer(required=True)
    alarm_subscription = AlarmSerializer(required=True)
    next_billing_at = serializers.SerializerMethodField()

    def get_next_billing_at(self, obj):
        return obj.next_billing_at()

    class Meta:
        model = Subscription
        exclude = ["user", "delete_on", "created_at", "updated_at"]

    def validate(self, data):
        error = {}

        category_type = data["plan"]["service"]["category"]["category_type"]
        service_id = data["plan"]["service"]["id"]
        plan_id = data["plan"]["id"]
        method_type = data["billing"]["type"]["method_type"]
        company_id = data["billing"]["company"]["id"]
        started_at = data["started_at"]
        expire_at = data["expire_at"]
        d_day = data["alarm_subscription"]["d_day"]

        # plan validation
        plan_list = Service.objects.get(id=service_id).plan_service.values_list("id", flat=True)
        if plan_id not in plan_list:
            error['plan'] = ["서비스에 해당 서비스 유형이 존재하지 않습니다."]

        # expire_at validation
        if expire_at:
            sub_last_day = calendar.monthrange(int(started_at.strftime("%Y")), int(started_at.strftime("%m")))[1]
            exp_last_day = calendar.monthrange(int(expire_at.strftime("%Y")), int(expire_at.strftime("%m")))[1]

            expire_at_error1 = started_at.strftime("%Y%m") >= expire_at.strftime("%Y%m")
            expire_at_error2 = int(started_at.strftime("%d")) != sub_last_day and started_at.strftime("%d") != expire_at.strftime("%d")
            expire_at_error3 = int(started_at.strftime("%d")) == sub_last_day and int(expire_at.strftime("%d")) != exp_last_day and sub_last_day != int(expire_at.strftime("%d"))
            expire_at_error4 = int(started_at.strftime("%d")) == sub_last_day and int(expire_at.strftime("%d")) == exp_last_day and sub_last_day < exp_last_day
  
            if (expire_at_error1) or (expire_at_error2) or (expire_at_error3) or (expire_at_error4):
                error['expire_at'] = ["만료예정일이 올바른 일자가 아닙니다."]

        # billing validation
        company_list = list(Company.objects.all().values_list('id', flat=True))
        credit_card = company_list[19:38]
        check_card = company_list[19:37]
        account = company_list[:19]
        easy_payment = company_list[38:52]
        mobile_payment = company_list[45:46] + company_list[52:57]

        error_company_message = ["결제유형에 해당 결제사가 존재하지 않습니다."]
    
        # 결제 유형이 '신용카드'인 경우 → '신용카드'에 해당하는 결제사가 아니라면 에러 발생
        if method_type == 1:
            if company_id not in credit_card:
                error['company'] = error_company_message
        # 결제 유형이 '체크카드'인 경우 → '체크카드'에 해당하는 결제사가 아니라면 에러 발생
        elif method_type == 2:
            if company_id not in check_card:
                error['company'] = error_company_message
        # 결제 유형이 '계좌이체'인 경우 → '계좌이체'에 해당하는 결제사가 아니라면 에러 발생
        elif method_type == 3:
            if company_id not in account:
                error['company'] = error_company_message
        # 결제 유형이 '간편결제'인 경우 → '간편결제'에 해당하는 결제사가 아니라면 에러 발생
        elif method_type == 4:
            if company_id not in easy_payment:
                error['company'] = error_company_message
        # 결제 유형이 '휴대폰결제'인 경우 → '휴대폰결제'에 해당하는 결제사가 아니라면 에러 발생
        elif method_type == 5:
            if company_id not in mobile_payment:
                error['company'] = error_company_message

        if error:
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        user = self.context.get("request").user

        plan_id = validated_data["plan"]["id"]
        method_type = validated_data["billing"]["type"]["method_type"]
        company_id = validated_data["billing"]["company"]["id"]
        started_at = validated_data["started_at"]
        expire_at = validated_data["expire_at"]
        d_day = validated_data["alarm_subscription"]["d_day"]

        plan = Plan.objects.get(id=plan_id)

        type_object = Type.objects.get(method_type=method_type)
        company = Company.objects.get(id=company_id)

        billing, is_created = Billing.objects.get_or_create(
            user = user,
            type = type_object,
            company = company
        )

        subscription = Subscription.objects.create(
            user=user,
            plan=plan, 
            billing=billing, 
            started_at=started_at,
        )

        if expire_at == '':
            subscription.expire_at = None
        else:
            subscription.expire_at=expire_at
            if expire_at < datetime.now().date():
                subscription.is_active = False

        subscription.save()

        alarm, is_created = Alarm.objects.get_or_create(
            d_day = d_day,
            subscription = subscription,
        )

        return subscription

    def update(self, instance, validated_data):

        user = self.context.get("request").user

        plan_id = validated_data["plan"]["id"]
        method_type = validated_data["billing"]["type"]["method_type"]
        company_id = validated_data["billing"]["company"]["id"]
        started_at = validated_data["started_at"]
        expire_at = validated_data["expire_at"]
        d_day = validated_data["alarm_subscription"]["d_day"]

        plan = Plan.objects.get(id=plan_id)

        type_object = Type.objects.get(method_type=method_type)
        company = Company.objects.get(id=company_id)

        billing, is_created = Billing.objects.get_or_create(
            user = user,
            type = type_object,
            company = company
        )
        
        instance.plan = plan
        instance.billing = billing
        instance.started_at = started_at

        if expire_at == '':
            instance.expire_at = None
        else:
            instance.expire_at=expire_at
            if expire_at < datetime.now().date():
                instance.is_active = False

        instance.save()

        alarm, is_created = Alarm.objects.get_or_create(
            d_day = d_day,
            subscription = instance,
        )

        return instance