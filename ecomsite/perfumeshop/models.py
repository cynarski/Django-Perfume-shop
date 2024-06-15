from django.db import models

# Create your models here.

class Perfume(models.Model):

    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.TextField()

    def __str__(self):
        return f"{self.brand} - {self.name}"
