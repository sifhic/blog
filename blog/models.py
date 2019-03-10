from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.unique_slug import unique_slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        unique_together = (("site", "slug"),)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            unique_slugify(self, self.name,self.site)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    def __str__(self):
        return self.heading

    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    heading = models.CharField(max_length=200)
    sub_heading = models.CharField(max_length=300,null=True,blank=True)
    slug = models.SlugField(max_length=100) # editable=False
    body = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='featured_images', blank=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=True)

    class Meta:
        unique_together = (("site", "slug"),)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug, 'id': self.id})

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            unique_slugify(self, self.heading,self.site)

        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    creator = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField()

    reply_to = models.ForeignKey('self', related_name='replies', null=True, blank=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField('date commented', auto_now_add=True)
    updated_at = models.DateTimeField('date edited', auto_now=True)

    def __str__(self):
        return self.text


class SiteProfile(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    about = models.TextField(blank=True)


    def __str__(self):
        return self.site.name