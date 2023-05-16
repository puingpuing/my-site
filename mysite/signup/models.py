from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.
'''
class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

class Registration(AbstractBaseUser):
    auto_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=155,null=False,default="")
    username = models.TextField(null=False, max_length=150, unique=True,default="") #varchar(128) NOT NULL
    password = models.CharField(null=False, max_length=128, default="")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_auth = models.BooleanField(default=False)
    joined_at = models.TimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'

    objects =  UserManager()

    class Meta:
        db_table = "registrations"
'''
class Registration(models.Model):

    #User._meta.get_field('email')._unique = True
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    updated_at = models.DateTimeField(auto_now = True)
    is_auth = models.BooleanField(default=False)

    class Meta:
        db_table = "registrations"
