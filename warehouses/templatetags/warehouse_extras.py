from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return float(value) - float(arg)
        except (ValueError, TypeError):
            return value

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return float(value) * float(arg)
        except (ValueError, TypeError):
            return value

@register.filter
def divide(value, arg):
    """Divide the value by the arg."""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        try:
            return float(value) / float(arg)
        except (ValueError, TypeError, ZeroDivisionError):
            return value

@register.filter
def modulo(value, arg):
    """Return the value modulo arg."""
    try:
        return int(value) % int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
