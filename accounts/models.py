from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Role(models.Model):
    full_name = models.CharField(max_length=100, unique=True)  
    slug = models.SlugField(max_length=100, unique=True, editable=False)       
    description = models.TextField(blank=True, null=True)      
    is_active = models.BooleanField(default=True)              

    def save(self, *args, **kwargs):
        base_slug = slugify(self.full_name)
        self.slug = base_slug.replace('-', '_')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} - {self.full_name}"


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} → {self.role.full_name if self.role else 'No Role'}"
