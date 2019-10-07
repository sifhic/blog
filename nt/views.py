from django.shortcuts import render, redirect, reverse
from nt.models import Config
from nt.forms import ConfigForm, SyncPostForm
import logging
from nt.tasks import sync_page

# Create your views here.

lgr = logging.getLogger(__name__)


def config_view(request):
    context = {}
    instance = Config.objects.first()

    if request.method == 'POST':
        form = ConfigForm(request.POST, instance=instance)
        lgr.debug(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            site = request.site
            site.name = form.cleaned_data['name']
            site.save()

            post.save()
            lgr.info("Created New Post: {}".format(post))
        else:
            lgr.error(form.errors)

        return redirect(reverse('admin:dashboard'))
    else:

        form = ConfigForm(instance=instance)
        sync_post_form = SyncPostForm()

    context = {
        'form': form,
        'post_sync_form': sync_post_form
    }

    return render(request, 'admin/notion_config.html', context)


def sync_view(request):
    if request.method == 'POST':
        form = SyncPostForm(request.POST)
        lgr.debug(request.POST)
        if form.is_valid():
            sync_page.delay(form.cleaned_data['url'])
        else:
            lgr.info(form.errors)

    return redirect(reverse('notion:config'))
