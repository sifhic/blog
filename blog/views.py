from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime

from .models import Post,Comment
def year():
    return datetime.now().year

# Create your views here.
def index(request):
    latest_post = Post.objects.filter(is_published=True).order_by('pub_date')[:5]
    context = {
        'latest_post': latest_post,
        'title':'Home',
        'year':year()
    }
    return render(request, 'blog/index.html', context)

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post,'title':post.heading}
    return render(request, 'blog/detail.html', context)


def comment(request, post_id):
    p=get_object_or_404(Post,pk=post_id)

    c=Comment()
    c.com_date=timezone.now()
    c.comment=request.POST['comment']
    p.comment_set.add(c)
    p.save()
    return HttpResponseRedirect(reverse('blog:post',args=(post_id,)))

def about(request):
    context={
        'title':'About',
        'year':year(),
        'message':'This is the about page'
    }
    return render(request,'blog/about.html',context)

def contact(request):
    context={
        'title':'Contacts',
        'year':year(),
        'message':'This is the Contacts page'
    }
    return render(request,'blog/contact.html',context)
    
def send_email(request):
    subject = request.POST.get('subject', '')
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if name and message and from_email:
        try:
            send_mail(subject, message, from_email, ['ndieksman@gmail.com'])
        except BadHeaderError:
            #return HttpResponseRedirect('/blog/contact')
            pass
        return HttpResponse('1')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')