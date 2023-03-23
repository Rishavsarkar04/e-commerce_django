from django import template
from app.models import Cart,Product

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_number(context):
    request = context['request']
    user = request.user
    cart_num = Cart.objects.filter(user=user).count()
    return cart_num
