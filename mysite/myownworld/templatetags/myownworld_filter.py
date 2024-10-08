import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sub(value, org):
    return value - org

# 마크다운 필터 등록
@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))