from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Profiles(models.Model):
    profile_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Employer(models.Model):
    profile_id = models.ForeignKey(Profiles, on_delete=CASCADE)
    name_of_employer = models.CharField(max_length=100)
    salary = models.IntegerField()
    position = models.CharField(max_length=100)
    income_date = models.CharField(max_length=100)
    income_frequency = models.IntegerField()
    employer_id = models.AutoField(primary_key=True)

class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    type_of_account = models.CharField(max_length=20)
    card_number = models.CharField(max_length=20)
    expiration_date = models.DateField()
    security_code = models.IntegerField()
    name_on_card = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    amount_on_card = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    credit_on_card = models.PositiveIntegerField(null=True)
    payment_date = models.CharField(max_length=100, null=True)

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(Accounts, on_delete=CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    date_occured = models.DateTimeField()
    name_of_recipient = models.CharField(max_length=100)

class ProfileAccountMapping(models.Model):
    date_connect = models.DateTimeField()
    account_id = models.ForeignKey(Accounts, on_delete=CASCADE)
    profile_id = models.ForeignKey(Profiles, on_delete=CASCADE)

class Budgets(models.Model):
    budget_id = models.AutoField(primary_key=True)
    timeframe = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    profile_id = models.ForeignKey(Profiles, on_delete=CASCADE)

class Subscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transactions, on_delete=CASCADE)
    recurring_payment_date = models.CharField
    active = models.BooleanField()
    profile_id = models.ForeignKey(Profiles, on_delete=CASCADE)

