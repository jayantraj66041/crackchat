from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=200, choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")))
    dp = models.ImageField(upload_to="dp/", default="dp/sample_dp.jpg", blank=True)
    cover_image = models.ImageField(upload_to="cover/", default="cover/sample_cover.jpg", blank=True)
    date_of_creation = models.DateTimeField(default=timezone.now)


class Post(models.Model):
    p_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to="post/", blank=True)
    post_desc = models.TextField()
    date_of_post = models.DateTimeField(default=timezone.now)


class Likes(models.Model):
    l_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_like = models.DateTimeField(default=timezone.now)


class Comments(models.Model):
    c_id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=200)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_comment = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    m_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
