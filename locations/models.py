from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

class Symbol(models.Model):
    image = models.ImageField()

class Country(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    population = models.IntegerField(default=0)
    flag = models.OneToOneField(Symbol, on_delete=models.DO_NOTHING)
    cities_count = models.IntegerField(default=0)
    users = models.ManyToManyField(User)

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        verbose_name_plural = 'Cities'


    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=City)
def post_save_city(instance, **kwargs):
    instance.country.cities_count += 1


@receiver(pre_delete, sender=City)
def pre_dlete_city(instance, **kwargs):
    instance.country.cities_count -= 1
    print(f"City has been delete")