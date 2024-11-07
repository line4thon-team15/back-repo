from django.contrib import admin
from .models import Service, PresentationImage, Member
# Register your models here.

admin.site.register(Service)
admin.site.register(PresentationImage)
admin.site.register(Member)