from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, gender, phone, batch, job_profile, password=None):
        if not email:
            raise ValueError("User must have email address")
        if not username:
            raise ValueError("User must have username")
        if not phone:
            raise ValueError("User must have phone number")
        
        user = self.model(
               email = self.normalize_email(email),
               username = username,
               gender = gender,
               phone = phone,
               batch = batch,
               job_profile = job_profile,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self ,email ,username, gender, phone, batch, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            gender = gender,
            phone = phone,
            batch = batch,
            password = password,
        )
        
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

# def get_profile_image_filepath(self):
#     return "images/"

# def get_deafult_profile_img():
#     return "imgs/"

class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username        = models.CharField(max_length=30, unique=True)
    phone           = models.BigIntegerField(unique=True)
    batch           = models.CharField(max_length=9)
    gender          = models.CharField(max_length=10)
    date_joined     = models.DateTimeField(verbose_name="data_joined", auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    hide_email      = models.BooleanField(default=True)
    bio             = models.CharField(max_length=40, default="Hey There, I am here useing AlumniSphere")
    job_profile     = models.CharField(max_length=20, default="Under Graduate")
    profile_image   = models.ImageField(upload_to="profile_img/", default="profile_img/default_profile_pic.png")
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email','password','phone','batch','gender']
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username
    # def get_profile_img_filename(self):
    #     return str(self.profile_image)[str(self.profile_image).index[f'profile_image/{self.pk}/']:]   
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perm(self, app_label):
        return True

class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    caption=models.TextField()
    image=models.ImageField(upload_to="img/")
    date = models.DateTimeField(verbose_name="data", auto_now_add=True, null=True)
    def __str__(self):
        return self.caption

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    
class Event(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    caption=models.TextField()
    image=models.ImageField(upload_to="event/")
    date = models.DateTimeField(verbose_name="data", auto_now_add=True, null=True)
    def __str__(self):
        return self.caption
    
class EventComment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    
    
    