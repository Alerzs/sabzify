from django import template

from website.jalali import format_jalali

register = template.Library()


@register.filter(name='jalali')
def jalali(value, arg=''):
    return format_jalali(value, with_time=str(arg) == 'time')
