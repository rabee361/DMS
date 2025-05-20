from finance.models import AccountMovement
from finance.models import Account
from finance.models import Currency

def create_movement(account, opposite_account, amount, currency, origin_type, origin_id):
    currency = Currency.objects.get(name=currency)
    account = Account.objects.get(name=account)
    opposite_account = Account.objects.get(name=opposite_account)
    movement = AccountMovement.objects.create(
        from_account=account,
        to_account=opposite_account,
        amount=amount,
        currency=currency,
        origin_type=origin_type,        
        origin_id=origin_id
    )
    return movement