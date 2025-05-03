from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])


@register.filter
def last4(phone_number):
    return phone_number[-4:] if phone_number else ""