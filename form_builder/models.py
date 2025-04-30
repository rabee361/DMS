from django.db import models
from utility.helper import generate_slug    
# Create your models here.


class CustomForm(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ar', 'Arabic'),
    ]
    TemplateChoice = [
        ('1', 'Template 1'),
        ('2', 'Template 2'),
        ('3', 'Template 3'),
    ]
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100,default='test')
    welcome = models.CharField(max_length=200,default='test')
    language = models.CharField(default="en", max_length=100, choices=LANGUAGE_CHOICES)
    slug = models.SlugField(max_length=100, default=generate_slug)
    template = models.CharField(max_length=100,choices=TemplateChoice,default='1')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

