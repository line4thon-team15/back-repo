from django.contrib import admin
from .models import Service, PresentationImage, Member, Part
# Register your models here.

admin.site.register(Service)
admin.site.register(PresentationImage)
admin.site.register(Member)
admin.site.register(Part)