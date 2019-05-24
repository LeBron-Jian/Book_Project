#_*_coding:utf-8_*_
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# 自定义过滤器
@register.filter
def path_filter(x):
    new_path = x.replace('book_list', 'add_book')
    return new_path

@register.filter
def id_filter(x):
    return int(x)

@register.filter
def user_tags(request):
    return request.session.get('user')

# 自定义标签
@register.filter
def update_path(current_path, book_id):
    new_path = current_path.replace('book_list', 'update_book/' + str(book_id))
    return new_path

# 自定义标签
@register.simple_tag
def multi_tags(x, y, z):
    return x*y*z

@register.simple_tag
def my_input(id, arg):
    result = "<input type='text' id='%s' class='%s'/>" %(id, arg,)
    return mark_safe(result)