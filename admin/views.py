from django.shortcuts import render,reverse,redirect
from admin.forms import SiteProfileForm
import logging
from blog.models import SiteProfile

lgr = logging.getLogger(__name__)

# Create your views here.

def dashboard(request):
    context = {}

    context['posts'] = Post.objects.all()
    context['categories'] = Category.objects.all()

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
    context = {}
    instance = SiteProfile.objects.first()

    if request.method == 'POST':
        form = SiteProfileForm(request.POST,instance=instance)
        lgr.debug(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            site = request.site
            site.name = form.cleaned_data['name']
            site.save()
            
            post.site = site
            post.save()
            lgr.info("Created New Post: {}".format(post))
        else:
            lgr.error(form.errors)

        return redirect(reverse('admin:dashboard'))
    else:

        form = SiteProfileForm(instance=instance)

    context = {
        'form': form
    }

    # site

    # site profile

    return render(request, 'admin/settings.html', context)
# end settings admin

