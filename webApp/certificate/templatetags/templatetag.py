from django import template

register = template.Library()


@register.filter
def mul(x, y):
    if not x:
        x = 0
    return round(x * y, 2)


@register.filter
def qianfenwei(x):
    return format(x, ',')


@register.filter
def iszi(x):
    if x == 1:
        x = '是'
    else:
        x = '否'

    return x