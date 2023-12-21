from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

#model for base school admin user (Ver0.1: Users are exclusivly organization admins as of now. Will ad independant teacher and parent login functionality)
class User(AbstractUser):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    #contact information
    phone = models.CharField(max_length=32, blank=True)
    social = models.CharField(max_length=64, blank=True, null=True) #for use with other contact servicers such as LINE, MESSENGER or WHATSAPP
    #school / org information
    school = models.ForeignKey('School', on_delete=models.SET_NULL, related_name='user', null=True, blank=True)
    tag = models.CharField(max_length=64, blank=True, null=True) #if they have a school ID or other form of required identifier.
    #permisions toggle
    is_admin = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=True)
    is_parent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    pass

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "altName": self.altName,
            "tag": self.tag,
            "social": self.social,
            "phone": self.phone,
        }

    def __str__(self):
        return f"{self.username}"

#TODO Teacher profile to add to school system

#TODO Parent profile to add to school system