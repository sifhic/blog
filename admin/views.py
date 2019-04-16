from django.shortcuts import render


# Create your views here.

def dashboard(request):
    context = {}

    return render(request, 'admin/dashboard.html', context)




# start categroies admin
from blog.models import Category
# Create your views here.
def category_list(request):
    categories = Category.objects.filter(site=request.site) .order_by('-created_at')[:5]
    context = {
        'categories': categories,
        'title':'Home',
    }
    return render(request, 'admin/categories/list.html', context)
# end category admin


# start blog admin
from blog.models import Post
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(site=request.site,is_published=True) .order_by('-created_at')[:5]
    context = {
        'posts': posts,
        'title':'Home',
    }
    return render(request, 'admin/posts/list.html', context)
# end blog admin



# start media admin
# Create your views here.
def media_list(request):
    context = {
    }
    return render(request, 'admin/posts/list.html', context)
# end media admin



# start users admin
# Create your views here.
def users_list(request):
    context = {
    }
    return render(request, 'admin/posts/list.html', context)
# end users admin



# start settings admin
# Create your views here.
def settings_list(request):
    context = {
    }
    return render(request, 'admin/posts/list.html', context)
# end settings admin

