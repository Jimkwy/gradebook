from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

#model for base school admin user (Ver0.1: Users are exclusivly organization admins as of now. Will ad independant teacher and parent login functionality)
class User(AbstractUser):
    phone = models.CharField(max_length=32, blank=True)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, related_name='user', null=True, blank=True)
    altName = models.CharField(max_length=64, blank=True, null=True)
    social = models.CharField(max_length=64, blank=True, null=True) #for use with other contact servicers such as LINE, MESSENGER or WHATSAPP
    code = models.CharField(max_length=64, blank=True, null=True) #if they have a school ID or other form of required identifier.
    timestamp = models.DateTimeField(auto_now_add=True)
    pass

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "altName": self.altName,
            "code": self.code,
            "social": self.social,
            "phone": self.phone,
        }

    def __str__(self):
        return f"{self.username}"

#TODO Teacher profile to add to school system

#TODO Parent profile to add to school system