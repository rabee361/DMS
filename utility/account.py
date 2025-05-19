from finance.models import AccountMovement
from finance.models import Account
from finance.models import Currency

def create_movement(account : Account , opposite_account : Account , amount : float , currency : Currency):
    movement = AccountMovement(account=account , opposite_account=opposite_account , amount=amount , currency=currency)
    movement.save()
    return movement