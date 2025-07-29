from django.db import models

# Create your models here.
class Continent(models.Model):
    name = models.CharField(max_length=100)
    results = models.JSONField()
    search_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.search_timestamp.strftime('%Y-%m-%d %H:%M:%S')}, {self.results}"