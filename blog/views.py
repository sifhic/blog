from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Post,Comment


# Create your views here.
def index(request):
    latest_post = Post.objects.order_by('pub_date')[:5]
    context = {'latest_post': latest_post,'title':'Home'}
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
    return HttpResponseRedirect(reverse('post',args=(post_id,)))