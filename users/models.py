from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings


# Create your models here.

class User(AbstractUser): 
    email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
    username = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(default="default.png", upload_to="profile_images/")
    kakao_id = models.CharField(max_length=256, null=True, blank=True)
    kakao_profile = models.URLField(default="", blank=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']
    
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')
   
