# -*- coding: utf-8 -*-

from django import template
from django.core.paginator import InvalidPage, EmptyPage, Paginator

register = template.Library()


@register.inclusion_tag('paginator.html')
def paginator(paginated_list):
    """
    Muestra el paginador estandar para servicios de una lista paginada
    """
    return {'paginated_list': paginated_list}