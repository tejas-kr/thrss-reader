from django.db import models

class RSS_links(models.Model):
    
    title = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=400, unique=True)

    def __str__(self):
        return f"{self.title} -> {self.url}"