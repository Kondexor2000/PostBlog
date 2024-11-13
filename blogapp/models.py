from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    encrypted_content = models.TextField(blank=True, null=True)  
    encryption_type = models.CharField(max_length=10, choices=[('RSA', 'RSA'), ('Caesar', 'Caesar')], default='RSA')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authorized_users = models.ManyToManyField(User, related_name="authorized_posts", blank=True)

    def __str__(self):
        return self.title