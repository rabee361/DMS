# your_app/templatetags/task_filters.py

from django import template

register = template.Library()

@register.filter
def count_by_status(tasks, status):
    return len([task for task in tasks if task.status == status])

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
def extract_unique_users(tasks):
    """Extract unique usernames from a queryset of tasks."""
    users = set()
    for task in tasks:
        if task.user and task.user.username:
            users.add(task.user.username)
    return list(users)