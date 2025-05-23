from django.db import models

class FileType(models.TextChoices):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    TEXT = 'txt'

class PaymentType(models.TextChoices):
    CASH = 'Cash'
    CREDIT_CARD = 'Credit Card'
    BANK_TRANSFER = 'Bank Transfer'

class PaymentCycle(models.TextChoices):
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'


class Language(models.TextChoices):
    ENGLISH = 'en'
    ARABIC = 'ar'

class AdditionDiscountType(models.TextChoices):
    ADDITION = 'إضافة'
    DISCOUNT = 'خصم'
        
class INVOICE_TYPES(models.TextChoices):
    SALES = 'Sales Invoice'
    PURCHASE = 'Purchase Invoice'
    SALES_RETURN = 'Sales Return Invoice'
    PURCHASE_RETURN = 'Purchase Return Invoice'

class CLIENT_TYPES(models.TextChoices):
    CUSTOMER = 'Customer'
    SUPPLIER = 'Supplier'

class PaymentStatus(models.TextChoices):
    PENDING = 'Pending'
    PARTIAL = 'Partially Paid'
    PAID = 'Paid'
    OVERDUE = 'Overdue'

class OriginType(models.TextChoices):
    SALARY = 'راتب'
    EXPENSE = 'مصروفات'
    LOAN = 'الإيداعات'

class PermissionLevel(models.TextChoices):
    PUBLIC = 'public'
    PRIVATE = 'private'
    USER = 'user'


class InvoiceType(models.TextChoices):
    SELL = 'مبيع'
    BUY = 'شراء'
    SELL_RETURN = 'مرتجع مبيع'
    BUY_RETURN = 'مرتجع شراء'
    INPUT = 'ادخال'
    OUTPUT = 'اخراج'

class DateFormat(models.TextChoices):
    DMY = 'dd/mm/yyyy'
    MDY = 'mm/dd/yyyy'
    YMD = 'yyyy/mm/dd'



class TimeFormat(models.TextChoices):
    TWELVE_HOUR = '12h'
    TWENTY_FOUR_HOUR = '24h'


class Progress(models.TextChoices):
    ZERO = '0%'
    QUARTER = '25%'
    HALF = '50%'
    THREE_QUARTERS = '75%'
    COMPLETE = '100%'


class Holiday(models.TextChoices):
    FULL_DAY = '8 Hours'
    HALF_DAY = '4 Hours'



class Absence(models.TextChoices):
    SICK_LEAVE = 'Sick Leave'
    NONE = '_'



class State(models.TextChoices):
    DONE = 'Done'
    REVIEW = 'Review'   
    INITIAL = 'Initial'


class Status(models.TextChoices):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'


class Priority(models.TextChoices):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MODERATOR = 'moderator', 'Moderator'
    NORMAL = 'normal', 'Normal User'

class SocialStatus(models.TextChoices):
    SINGLE = 'Single'
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    WIDOWED = 'Widowed'
