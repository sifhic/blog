from django.db import models
from django.contrib.auth.admin import User

    

class Post(models.Model):
    def __str__(self):
        return self.heading
    creator=models.ForeignKey(User)
    heading=models.CharField(max_length=200)
    sub_heading=models.CharField(max_length=300)
    body=models.TextField()
    is_published = models.BooleanField(default=0)
    featured_image = models.ImageField(upload_to='featured_images')
    pub_date=models.DateTimeField('date published', auto_now_add=True)
    
# Create your models here.
class Tag(models.Model):
    name=models.CharField(max_length=60)
    post = models.ManyToManyField(Post,related_name="tags")

class Comment(models.Model):
    def __str__(self):
        return self.comment
    comment=models.CharField(max_length=400)
    post_id=models.ForeignKey(Post)
    com_date=models.DateTimeField('date commented', auto_now_add=True)