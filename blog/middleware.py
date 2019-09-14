from django.conf import settings
from blog.models import Post,Category,SiteProfile, Tag
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
import logging

lgr = logging.getLogger(__name__)


class SiteMetaMiddleware(MiddlewareMixin):
    """Middleware class that retrieves the site metadata
    """

    def process_request(self, request):
        """
        """
        # todo filter by site

        # todo is this required?, there is already request.site
        site_profile = SiteProfile.objects.last()
        categories = Category.objects.exclude(name='default')
        popular_posts = Post.objects.all()[:5]
        tags = Tag.objects.all()

        request.tags = tags
        request.site_profile = site_profile
        request.display_categories = categories.exists()
        request.categories = categories
        request.popular_posts = popular_posts
