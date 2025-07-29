from django.db import models
from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
    
    def __str__(self):
        return self.title