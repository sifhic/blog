from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.unique_slug import unique_slugify
from django.contrib.postgres.fields import JSONField



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

import markdown
from django.template.loader import render_to_string
from pygments import highlight

from pygments.formatters import HtmlFormatter

class Block(models.Model):
    TEXT = 1
    DIVIDER = 2
    BULLETED_LIST = 3
    IMAGE = 4
    QUOTE = 5
    HEADER = 6
    SUB_HEADER = 7
    SUB_SUB_HEADER = 8
    CODE = 9
    TODO = 10
    COLUMN_LIST_BLOCK = 11
    COLUMN_BLOCK = 12

    BLOCK_CHOICES = (
        (TEXT,'TEXT'),
        (DIVIDER,'DIVIDER'),
        (BULLETED_LIST,'BULLETED LIST'),
        (IMAGE,'IMAGE'),
        (QUOTE,'QUOTE'),
        (HEADER,'HEADER'),
        (SUB_HEADER,'SUB HEADER'),
        (SUB_SUB_HEADER,'SUB SUB HEADER'),
        (CODE,'CODE'),
        (TODO,'TODO'),
        (COLUMN_LIST_BLOCK,'ColumnListBlock'),
        (COLUMN_BLOCK,'ColumnBlock'),
    )


    type = models.PositiveSmallIntegerField(choices=BLOCK_CHOICES,default=TEXT)
    config = JSONField(default=dict)

    children = models.ManyToManyField('self',symmetrical=False)

    def child_blocks(self):
        return self.children.order_by('id')

    @property
    def content(self):
        return self.config['content'] if 'content' in self.config else ''

    def rendered(self):
        if self.type == Block.BULLETED_LIST:
            rendered = render_to_string('blog/post/blocks/bulleted-list.html', {'item': self.content})
            return  rendered

        elif self.type == Block.TEXT:
            return markdown.markdown(self.content) if len(self.content) else '<p><br></p>'

        elif self.type == Block.COLUMN_LIST_BLOCK:
            rendered = render_to_string('blog/post/blocks/column-list-block.html', {'block':self})
            return rendered

        elif self.type == Block.COLUMN_BLOCK:
            rendered = render_to_string('blog/post/blocks/column-block.html', {'block':self})
            return rendered

        elif self.type == Block.TODO:
            rendered = render_to_string('blog/post/blocks/todo.html', {
                'item': self.content,
                'checked':self.config['checked']
            })
            return rendered

        elif self.type == Block.HEADER:
            return '<h1>{}</h1>'.format(self.content)

        elif self.type == Block.SUB_HEADER:
            return '<h2>{}</h2>'.format(self.content)

        elif self.type == Block.SUB_SUB_HEADER:
            return '<h3>{}</h3>'.format(self.content)

        elif self.type == Block.IMAGE:
            return '<img src="{}" alt="{}" class="img-fluid">'.format(
                self.config['display_source'],
                self.config['caption']
            )

        elif self.type == Block.QUOTE:
            return '<blockquote>{}</blockquote>'.format(self.content)

        elif self.type == Block.DIVIDER:
            return '<hr>'

        elif self.type == Block.CODE:
            code = self.content
            if self.config['language'] == 'python':
                pass

            from pygments.lexers import PythonLexer
            rendered = highlight(code, PythonLexer(), HtmlFormatter())

            return rendered

        return '<strong style="color:red">{}</strong>'.format( self.get_type_display())

    def __str__(self):
        return '{}'.format(self.get_type_display())

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

    body = models.ManyToManyField(Block,blank=True)

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
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

    def blocks(self):
        return self.body.order_by('id')


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    creator = models.ForeignKey(Contact,on_delete=models.CASCADE)
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


class Message(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    sender = models.ForeignKey(Contact,on_delete=models.CASCADE)
