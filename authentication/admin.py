from django.contrib import admin
from .models import Email,User


# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    # todo account_profile should return fk model __str__
    list_display = ['email','username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']
    # list_filter = ('account_type',)


admin.site.register(User, AccountAdmin)
admin.site.register(Email)
