from django.db import models
import time

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    description = models.CharField(max_length=256, default=' ')
    profile_picture = models.CharField(max_length=256, default=' ')
    cover_photo = models.CharField(max_length=256, default=' ')
    date_of_joining = models.DateTimeField(auto_now=True)
    requests_sent_to_groups = models.CharField(max_length=128, null=True, default='')
    pending_requests_to_groups = models.CharField(max_length=128, null=True, default='')
    approved_requests = models.CharField(max_length=128, null=True, default='')
    USER_TYPE_CHOICES = (
        ('simple_user', 'Simple User'),
        ('group_member', 'Group Member'),
        ('registered', 'Registered'),
        ('admin', 'Admin')
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='simple_user')

    @classmethod
    def insert_user(cls, name, age, email, contact, password, country, description,profile_picture,
                    cover_photo):
        date_of_joining = int(time.time())
        user_type = 'Simple User'
        user = cls(name=name, age=age, email=email, contact=contact, password=password,
                   country=country, date_of_joining=date_of_joining, user_type=user_type,
                   description=description, profile_picture=profile_picture,
                   cover_photo=cover_photo
                   )
        user.save()
        return user

class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

class Post(models.Model):
    user_id = models.IntegerField()
    user_img = models.CharField(max_length=256, default=True)
    user_name = models.CharField(max_length=256, default=True)
    post_text = models.CharField(max_length=1056, default=True)
    post_image = models.CharField(max_length=256, default='', null=True)
    num_of_likes = models.IntegerField(default=0)
    num_of_dislikes = models.IntegerField(default=0)
    liked_by = models.CharField(max_length=200)
    disliked_by = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

class Problems(models.Model):
    Prob_img = models.CharField(max_length=256, default=True)
    Prob_name = models.CharField(max_length=256, default=True)
    solvedby=models.IntegerField(default=0)
    Prob_description = models.TextField(default='')
    Prob_isactive=models.CharField(max_length=256, default='True')
    output=models.CharField(max_length=512, default='')
    solution=models.TextField(default='')
    Prob_level=models.IntegerField(default=1)

class Results(models.Model):
    user_id = models.IntegerField()
    prob_id=models.IntegerField()
    result=models.CharField(max_length=256, default='False')
