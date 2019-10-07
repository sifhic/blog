from django.db import models
from blog.models import Post, Block as BlogBlock
from django.contrib.sites.models import Site


# Create your models here.

class Config(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    token = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return '{}'.format(self.site)


class Block(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null=True, blank=True,related_name='nt_block')
    block = models.OneToOneField(BlogBlock, on_delete=models.CASCADE, null=True, blank=True,related_name='nt_block')
    config = models.ForeignKey(Config, on_delete=models.CASCADE)

    updated_run = models.DateTimeField('Notion date run', null=True, blank=True)
    updated_at = models.DateTimeField('Notion date updated', null=True, blank=True)
    reference = models.CharField(unique=True, blank=True, null=True, max_length=100)

    def __str__(self):
        return '{} {} {}'.format(self.config, self.post, self.block)
