from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profiles)
admin.site.register(Accounts)
admin.site.register(Transactions)
admin.site.register(Subscriptions)
admin.site.register(Budgets)
admin.site.register(ProfileAccountMapping)
admin.site.register(Employer)
