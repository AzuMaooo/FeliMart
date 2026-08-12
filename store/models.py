from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('toy', 'Toy'),
        ('accessory', 'Accessory'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    RARITY_CHOICES = [
        ('common', 'Common'),
        ('rare', 'Rare'),
    ]
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)

    def __str__(self):
        return self.name