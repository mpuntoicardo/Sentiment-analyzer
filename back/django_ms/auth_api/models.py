from django.db import models
from django.contrib.auth.models import User

class Search(models.Model):
    results = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favorite = models.ForeignKey(User, on_delete=models.CASCADE, null=True)