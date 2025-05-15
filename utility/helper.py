from datetime import datetime
import random
import string


def change_format(date: str) -> str:
    original = datetime.strptime(str(date).replace('/', '-').strip(), '%m-%d-%Y').date()
    new_format = original.strftime('%Y-%m-%d')
    return new_format

def reverse_format(date):
    original = datetime.strptime(str(date), '%Y-%m-%d').date()
    new_format = original.strftime('%m-%d-%Y')
    return new_format

def generate_slug(name: str = "") -> str:
    """Generate an 8-character slug of random letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
