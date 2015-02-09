
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have a valid authentication name.')
        
        if not kwargs.get('email'):
            raise ValueError('User must have a valid email.')
        
        if not kwargs.get('fullname'):
            raise ValueError('User must have a valid full name.')
        
        if not kwargs.get('birthday'):
            raise ValueError('User must have a valid birthday.')
        
        if not kwargs.get('sex'):
            raise ValueError('User must have a valid sex.')
        
        user = self.model(username=username, 
                             email = self.normalize_email(kwargs.get('email')),
                             fullname =kwargs.get('fullname'),
                             birthday = kwargs.get('birthday'),
                             sex = kwargs.get('sex'))
        
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, username, password=None, **kwargs):
        account = self.create_user(username, password, **kwargs)
        account.is_admin = True
        account.save()
        
        return account
    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)    
    username = models.CharField(max_length=40, unique=True)
    fullname = models.CharField(max_length=80, blank=False)
    birthday = models.DateField(blank=False)
    SEX_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=False)
    tagline = models.CharField(max_length=128, blank=True)
    photo = models.ImageField(upload_to='authentication/%Y/%m/%d', blank=True)
    
    is_admin = models.BooleanField(default=False)
    
    updated_on = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname', 'birthday', 'sex']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.fullname;
    
    def get_short_name(self):
        return self.fullname;
                        
    class Meta:
        db_table = 'users'