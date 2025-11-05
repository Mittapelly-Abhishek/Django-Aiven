from django.db import models

# Create your models here.


class UsersTable(models.Model):
    user_id=models.IntegerField(primary_key=True)
    user_name=models.CharField(max_length=50,null=False)
    user_email=models.EmailField(max_length=50,default="emp@org.com")
    user_mob=models.CharField(max_length=10,unique=True)
    profile_pic=models.URLField(default="empty")

    def __str__(self):
        return self.name