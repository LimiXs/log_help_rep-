from django import template
from info_assist.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    return menu
