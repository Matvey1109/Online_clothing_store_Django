from django import template
from store.models import *

register = template.Library()

@register.simple_tag(name='getcatsurl')
def get_categoriesURL(gender, cat):
    return reverse('category', kwargs={'category_slug': cat.slug, 'gender_slug': gender.slug})
