from django import template

register = template.Library()

@register.filter
def get_item(obj, key):
    """
    Template filter to access dictionary items by key or object attributes
    
    Usage in templates:
    {{ my_dict|get_item:key_variable }}
    {{ my_object|get_item:'attribute_name' }}
    """
    try:
        # First try to access as dictionary
        if isinstance(obj, dict):
            return obj.get(key, '')
        # Then try to access as object attribute
        else:
            return getattr(obj, key, '')
    except (TypeError, AttributeError):
        # Return empty string if access fails
        return '' 

@register.filter
def intdiv(value, arg):
    """
    Integer division filter
    
    Usage in templates:
    {{ value|intdiv:arg }}
    
    Example:
    {{ 10|intdiv:3 }} will return 3
    """
    try:
        return int(int(value) / int(arg))
    except (ValueError, ZeroDivisionError):
        return 0 
    


@register.filter
def range_filter(number):
    """
    Returns a list containing range made from given number
    Usage: {% for i in number|range_filter %}
    """
    return range(int(number))
