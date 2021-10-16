# Generated by Django 3.2.8 on 2021-10-16 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_of_account', models.CharField(max_length=20)),
                ('card_number', models.CharField(max_length=20)),
                ('expiration_date', models.DateField()),
                ('security_code', models.IntegerField()),
                ('name_on_card', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=100)),
                ('amount_on_card', models.DecimalField(decimal_places=2, max_digits=100, null=True)),
                ('credit_on_card', models.PositiveIntegerField(null=True)),
                ('payment_date', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100, null=True)),
                ('date_occured', models.DateTimeField()),
                ('name_of_recipient', models.CharField(max_length=100)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.accounts')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('subscription_id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField()),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.profiles')),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.transactions')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAccountMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_connect', models.DateTimeField()),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.accounts')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('name_of_employer', models.CharField(max_length=100)),
                ('salary', models.IntegerField()),
                ('position', models.CharField(max_length=100)),
                ('income_date', models.CharField(max_length=100)),
                ('income_frequency', models.IntegerField()),
                ('employer_id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Budgets',
            fields=[
                ('budget_id', models.AutoField(primary_key=True, serialize=False)),
                ('timeframe', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100, null=True)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finfreedom_frontend.profiles')),
            ],
        ),
    ]
