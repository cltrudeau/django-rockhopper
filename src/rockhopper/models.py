# rockhopper/models.py
from django.db import models

# ===========================================================================

class Tag(models.Model):
    name = models.CharField(max_length=20)


class Page(models.Model):
    """Stores the contents of a page to be displayed to the user"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    filename = models.CharField(max_length=200, blank=True, default='')
    filehash = models.CharField(max_length=64, blank=True, default='')
    is_private = models.BooleanField(default=False)

    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()
    pubdate = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
