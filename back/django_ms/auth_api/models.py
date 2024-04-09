from django.db import models
from django.contrib.auth.models import User

class Search(models.Model):
    results = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_searches')
    is_favorite = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='favorite_searches')

class Url(models.Model):
    name = models.CharField(max_length=255)
    search_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Keyword(models.Model):
    word = models.CharField(max_length=255)
    search_id = models.ForeignKey(User, on_delete=models.CASCADE)