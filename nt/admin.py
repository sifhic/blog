from django.contrib import admin
from nt.models import Config,Block
# Register your models here.

admin.site.register([Block,Config])