from urllib.parse import urljoin

from django import template
from django.conf import settings
from dynamic_preferences.registries import global_preferences_registry

register = template.Library()


@register.simple_tag
def available_management_settings_sections(request):
    from ephios.core.views.settings import get_available_management_settings_sections

    return get_available_management_settings_sections(request)


@register.simple_tag
def oidc_client_enabled():
    return settings.ENABLE_OIDC_CLIENT


@register.simple_tag
def site_url():
    return settings.GET_SITE_URL()


@register.simple_tag
def organization_name():
    return global_preferences_registry.manager().get("general__organization_name")


@register.filter
def make_absolute(location):
    return urljoin(settings.GET_SITE_URL(), location)
