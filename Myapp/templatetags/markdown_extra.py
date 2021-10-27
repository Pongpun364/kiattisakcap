# เอาไว้ไปโหลดหน้า html ของ testmd.html ie. {% load markdown_extra %}
from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

@register.filter()
@stringfilter

def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
