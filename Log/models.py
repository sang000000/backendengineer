from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role = models.CharField("role",max_length=20, default="USER")

class User(AbstractUser):

    roles = models.ForeignKey(Role,on_delete=models.CASCADE,related_name="roles",null=True, blank=True)
    username = models.CharField("username",max_length=10,unique=True)
    password = models.CharField("password",max_length=15)
    nickname = models.CharField("nickname",max_length=8,unique=True)
    
    def save(self, *args, **kwargs):
        if not self.roles:  # 역할이 없을 경우 기본값 부여
            self.roles = Role.objects.get_or_create(role="USER")[0]
        super().save(*args, **kwargs)
