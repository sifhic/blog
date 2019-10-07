from django import VERSION as DJANGO_VERSION
from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import escape_uri_path

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, view_name, css_class=None, strict=None, *args, **kwargs):
    """
    Renders the given CSS class if the request path matches the path of the view.
    :param context: The context where the tag was called. Used to access the request object.
    :param view_name: The name of the view (include namespaces if any).
    :param css_class: The CSS class to render.
    :param strict: If True, the tag will perform an exact match with the request path.
    :return:
    """
    if css_class is None:
        css_class = getattr(settings, 'ACTIVE_LINK_CSS_CLASS', 'active')

    if strict is None:
        strict = getattr(settings, 'ACTIVE_LINK_STRICT', False)

    request = context.get('request')
    if request is None:
        # Can't work without the request object.
        return ''
    path = reverse(view_name, args=args, kwargs=kwargs)
    request_path = escape_uri_path(request.path)
    # print(' {} {} - {}'.format(view_name,path,request_path))
    if strict:
        active = request_path == path
    else:
        active = request_path.find(path) == 0
    if active:
        return css_class
    return ''
