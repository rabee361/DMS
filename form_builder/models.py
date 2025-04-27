from django.db import models

# Create your models here.


class CustomForm(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ar', 'Arabic'),
    ]
    name = models.CharField(max_length=100)
    language = models.CharField(default="en", max_length=100, choices=LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

