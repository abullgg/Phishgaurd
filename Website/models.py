from django.db import models

# Create your models here.
class Phishing(models.Model):
    url=models.TextField()
    output=models.CharField(max_length=500)
    def __str__(self):
        return f"{self.url} → {self.output}"

    
