from django.db import models
from django.urls import reverse
from decimal import Decimal
# Create your models here.


class Storage(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_SiO2 = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_Fe = models.DecimalField(max_digits=10, decimal_places=2)
    coordinates = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'storage'
        verbose_name_plural = 'storages'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    
    @property
    def percentageFe(self):
            return "{:.1%}".format(
                self.percentage_Fe)
                
    @property
    def percentageSiO2(self):
            return "{:.1%}".format(
                self.percentage_SiO2)


class Truck(models.Model):
    storage = models.ForeignKey(
        Storage,
        related_name='Storage',
        on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    model = models.CharField(max_length=200, db_index=True)
    carrying_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    max_carrying_capacity = models.DecimalField(
        max_digits=10, decimal_places=2)
    percentage_SiO2 = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_Fe = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('name',)
        verbose_name = 'truck'
        verbose_name_plural = 'trucks'

    def __str__(self):
        return self.name

    @property
    def overload(self):
        if(self.carrying_capacity <= self.max_carrying_capacity):
            return 0
        else:
            return "{:.1%}".format(
                self.carrying_capacity / self.max_carrying_capacity)
    
    @property
    def percentageFe(self):
            return "{:.1%}".format(
                self.percentage_Fe)

    @property
    def percentageSiO2(self):
            return "{:.1%}".format(
                self.percentage_SiO2)


    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
