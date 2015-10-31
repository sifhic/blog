from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class Post(models.Model):
    def __str__(self):
        return self.heading
    creator=models.ForeignKey(User)
    heading=models.CharField(max_length=200)
    body=models.TextField()
    pub_date=models.DateTimeField('date published')

class Comment(models.Model):
    def __str__(self):
        return self.comment
    comment=models.CharField(max_length=400)
    post_id=models.ForeignKey(Post)
    com_date=models.DateTimeField('date commented')