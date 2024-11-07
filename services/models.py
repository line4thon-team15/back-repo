from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=30, blank=True, null=True)
    team = models.IntegerField(unique=True)
    content = models.CharField(max_length=300, blank=True, null=True) #일단은 300자로 나중에 변경
    site_url = models.CharField(max_length=100, blank=True, null=True)
    
    thumbnail_image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PresentationImage(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path)

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='member')
    member = models.CharField(max_length=30)
    part = models.CharField(max_length=30, null=True, blank=True)

class Part(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='part')
    part = models.CharField(max_length=30)