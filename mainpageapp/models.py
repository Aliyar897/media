# In models.py

from django.db import models

class ScrapedNewsData(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    summary = models.TextField(null=True, blank=True)
    summary_status = models.BooleanField(default=False, null=True, blank=True)
    date_published = models.DateTimeField()
    image = models.URLField()
    link = models.URLField()
    category = models.CharField(max_length=40, null=True)
    source = models.CharField(max_length=40, null=True)
    def __str__(self):
        return self.title
    
    
class States(models.Model):
    post = models.ForeignKey(ScrapedNewsData, on_delete=models.CASCADE, related_name='states')
    like_count = models.IntegerField(default=0)
    like_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post.title} - Likes: {self.like_count}, Liked: {self.like_status}"