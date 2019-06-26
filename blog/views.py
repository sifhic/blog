from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

from blog.models import Post,Comment,Category
from blog.forms import PostForm,CategoryForm


import logging
lgr = logging.getLogger(__name__)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def post_list(request):
    page = request.GET.get('page', 1)
    posts_queryset = Post.objects.filter(site=request.site,is_published=True).order_by('-created_at')

    q = request.GET.get('q', None)
    if q:
        posts_queryset = posts_queryset.filter(heading__icontains=q)

    paginator = Paginator(posts_queryset, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'title':'Home',
    }
    return render(request, 'blog/post/list.html', context)


def category_list(request):
    categories = Category.objects.filter() # .order_by('-created_at')[:5]
    context = {
        'categories': categories,
        'title':'Home'
    }
    return render(request, 'blog/category/list.html', context)


def post_view(request, post_pk, slug = None):
    post = get_object_or_404(Post, slug=slug)

    post.body.all()
    context = {'post': post,'title':post.heading}
    return render(request, 'blog/post/view.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        lgr.info(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.site = request.site
            post.save()
            lgr.info("Created New Post: {}".format(post))

        return redirect(reverse('admin:posts:list'))
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'blog/post/create.html', context)


def post_edit(request,post_pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        lgr.info(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.site = request.site
            post.save()
            lgr.info("Created New Post: {}".format(post))

        return redirect(reverse('admin:posts:list'))
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'blog/post/create.html', context)


def post_delete(request,post_pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        lgr.info(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.site = request.site
            post.save()
            lgr.info("Created New Post: {}".format(post))

        return redirect(reverse('admin:posts:list'))
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'blog/post/create.html', context)


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.site = request.site

            category.save()
            lgr.info("Created New Category: {}".format(category))

        return redirect(reverse('blog:categories:list'))
    else:
        form = CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'blog/category/create.html', context)


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
        'message':'This is the about page'
    }
    return render(request,'blog/about.html',context)


def contact(request):
    context={
        'title':'Contacts',
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
