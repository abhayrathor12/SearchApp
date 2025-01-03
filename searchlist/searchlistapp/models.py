from django.db import models

# Create your models here.


class Productlist(models.Model):
    model = models.CharField(max_length=100)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.model
