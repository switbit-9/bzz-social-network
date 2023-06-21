from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


GENDER_CHOICES =[
    ("m", "Male"),
    ("f", "Female"),
]


# Create your models here.
class User(AbstractUser):
    last_name = None
    first_name = None
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, validators=[password_validation.validate_password])
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='m')
    birthday = models.DateField(max_length=100, default=timezone.localdate, null=True, blank=True)
    createdDate = models.DateTimeField(max_length=100, default=timezone.now)
    email = models.EmailField(blank=None, unique=True, primary_key=False)

    REQUIRED_FIELDS = ['email', 'firstName', 'lastName']

    class Meta:
        db_table = 'accounts'

    def __repr__(self):
        return self.username



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name='followed_by',
                                     symmetrical=False, # You can follow smb and dont have to follow you back
                                     blank=True,
                                     )
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    bio = models.TextField(max_length=100, null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.user.username


#Create Profile when New User Sign Up
# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id]) #Follow youself
        user_profile.save()


post_save.connect(create_profile, sender=User)