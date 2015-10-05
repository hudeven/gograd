from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

class ResearcherProfile(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    interests = models.TextField()
    photo_url = models.TextField()
    critical_text = models.TextField()
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.url


