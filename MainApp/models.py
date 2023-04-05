import datetime
from django.db import models
from django.contrib.auth.models import User

LANG_CHOICES = (
    ("py", "python"),
    ("js", "javascript"),
    ("C++", "C++"),
)


class Comment(models.Model):
    text = models.TextField(max_length=2000)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    snippet = models.ForeignKey(to='Snippet', on_delete=models.CASCADE, related_name="comments")


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICES)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return f"Snippet: {self.name}"
