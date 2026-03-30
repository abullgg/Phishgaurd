from django.db import models

# Create your models here.
class Phishing(models.Model):
    url = models.TextField()
    output = models.CharField(max_length=500)
    confidence_score = models.FloatField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} → {self.output}"
