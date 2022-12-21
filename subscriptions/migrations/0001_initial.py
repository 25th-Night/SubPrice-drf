# Generated by Django 3.2.13 on 2022-11-27 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
            ],
            options={
                'verbose_name': '결제수단',
                'verbose_name_plural': '결제수단 목록',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
                ('category_type', models.PositiveSmallIntegerField(choices=[(1, 'OTT'), (2, '음악'), (3, '도서'), (4, '유통'), (5, '소프트웨어'), (6, '정기배송'), (7, '렌탈')], unique=True, verbose_name='카테고리 종류')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리 목록',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
                ('company', models.CharField(max_length=50, verbose_name='결제사')),
            ],
            options={
                'verbose_name': '결제사',
                'verbose_name_plural': '결제사 목록',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
                ('name', models.CharField(max_length=50, verbose_name='구독플랜')),
                ('price', models.PositiveIntegerField(verbose_name='가격')),
            ],
            options={
                'verbose_name': '구독 플랜',
                'verbose_name_plural': '구독 플랜 목록',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
                ('method_type', models.PositiveSmallIntegerField(choices=[(1, '신용카드'), (2, '체크카드'), (3, '계좌이체'), (4, '간편결제'), (5, '휴대폰결제')], unique=True, verbose_name='결제유형')),
                ('company', models.ManyToManyField(related_name='type_company', through='subscriptions.Billing', to='subscriptions.Company', verbose_name='결제사')),
            ],
            options={
                'verbose_name': '결제유형',
                'verbose_name_plural': '결제유형 목록',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
                ('started_at', models.DateField(verbose_name='최초 구독일')),
                ('expire_at', models.DateField(blank=True, null=True, verbose_name='구독 만료일')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성 여부')),
                ('delete_on', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('billing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_billing', to='subscriptions.billing', verbose_name='결제 정보')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_plan', to='subscriptions.plan', verbose_name='구독플랜')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_user', to='users.user', verbose_name='사용자')),
            ],
            options={
                'verbose_name': '사용자 구독 정보',
                'verbose_name_plural': '사용자 구독 정보 목록',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='갱신일')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='서비스명')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_category', to='subscriptions.category', verbose_name='서비스')),
            ],
            options={
                'verbose_name': '서비스',
                'verbose_name_plural': '서비스 목록',
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_service', to='subscriptions.service', verbose_name='서비스'),
        ),
        migrations.AddField(
            model_name='company',
            name='type',
            field=models.ManyToManyField(related_name='company_type', through='subscriptions.Billing', to='subscriptions.Type', verbose_name='결제수단'),
        ),
        migrations.AddField(
            model_name='billing',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_company', to='subscriptions.company', verbose_name='결제사'),
        ),
        migrations.AddField(
            model_name='billing',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_type', to='subscriptions.type', verbose_name='결제수단'),
        ),
        migrations.AddField(
            model_name='billing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_user', to='users.user', verbose_name='사용자'),
        ),
    ]