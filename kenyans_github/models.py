from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.admin import User
from django.dispatch import receiver
import os
import json
import urllib.request,urllib.parse,urllib.error
# Create your models here.


class GitHubKenyansWatcher(models.Model):
    user = models.OneToOneField(User, unique=True)
    token = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=50,null=False)


class GitHubApi(object):

    api_host = "https://api.github.com"
    api_account = GitHubKenyansWatcher.objects.get(pk=1)

    auth_header = {'Authorization': 'token %s' % api_account.token}


    def response(self, request):
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            if hasattr(e,'reason'):
                print('Failed to reach a server')
                print('Reason ', e.reason)
            elif hasattr(e,'code'):
                print('Server couldn\'t fullfill the request')
                print('Error code ', e.code)

        else:
            #response.info().header
            return response.read().decode()

    def put(self, endpoint):
        request = urllib.request.Request(self.api_host+endpoint, None, self.auth_header, method='PUT')
        return self.response(request)

    def delete(self, endpoint):
        request = urllib.request.Request(self.api_host+endpoint, None, self.auth_header, method='DELETE')
        return self.response(request)


    def get(self,endpoint):
        #request = urllib.request.Request(endpoint)
        #request.add_header('Authorization', 'token %s' % token)
        return self.response(urllib.request.Request(self.api_host+endpoint, None, self.auth_header))


    def get_user(self, username):
        return self.get('/user/'+username)

    def activities(self):
        return self.get('/users/'+self.api_account.username+'/received_events')


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_users(self):
        api=GitHubApi()
        q=urllib.parse.urlencode({'q':'location:'+self.name})
        data=json.loads(api.get('/search/users?'+q))#todo check if response

        #with open(os.path.dirname(__file__) + '/seacrhlocation', encoding='utf-8') as rec_events:
        #    data = json.loads(rec_events.read())

        for i in data['items']:
            gu= GitHubUser()
            gu.username=i['login']
            gu.location_id=self
            print(gu,end='\n')
            gu.save()

        self.count = data['total_count']
        self.save()

@receiver(post_save, sender=Location)
def update_location_users(sender, instance, **kwargs):
    instance.update_users()


class GitHubUser(models.Model):
    username = models.CharField(max_length=100,unique=True)
    location = models.ForeignKey(Location)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def follow(self):
        #PUT /user/following/:username
        api=GitHubApi()
        api.put('/user/following/'+self.username)

    def un_follow(self):
        #DELETE /user/following/:username
        api=GitHubApi()
        api.delete('/user/following/'+self.username)

    def close(self):
        self.is_open = False
        self.save()

    def open(self):
        self.is_open = True
        self.save()


