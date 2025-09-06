from django.db import models
from accounts.models import User
from django.utils.text import slugify


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        blank=True,
        on_delete=models.CASCADE,
        related_name="childs"
    )
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("published", "Published"),
        ("rejected", "Rejected"),
    )


    title = models.CharField(max_length=200, verbose_name="عنوان")
    image = models.ImageField(upload_to="blogs/", verbose_name="عکس")
    body = models.TextField(verbose_name="مقاله")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="اسلاگ")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_premium = models.BooleanField(default=False, verbose_name="مقاله ویژه")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["created_at"]
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
    

    def __str__(self):
        return f"کامنت از {self.user}"
    

    @property
    def is_reply(self):
        return self.parent is not None