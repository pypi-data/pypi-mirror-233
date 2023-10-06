from django.template import Library
from baykeshop.apps.shop.models import BaykeShopCategory

register = Library()

@register.inclusion_tag("system/pagination.html")
def pagination(page_obj):
    return {
        "count": page_obj.paginator.count,
        "current": page_obj.number,
        "per_page":page_obj.paginator.per_page
    }

@register.simple_tag
def shopcates():
    return BaykeShopCategory.objects.filter(parent__isnull=True, is_nav=True)

@register.filter
def multiply(value, arg):
    from decimal import Decimal
    return Decimal(value) * int(arg)