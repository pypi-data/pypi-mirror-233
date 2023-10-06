"""
Defines a (slightly silly) Django model that we can use in unit tests.
"""
from django.db import models


class Specie(models.Model):
    common_name = models.CharField(
        db_index=True,
        max_length=40,
        unique=True,
    )

    binomial_name = models.CharField(
        db_index=True,
        max_length=40,
        unique=True,
    )

    is_cuddly = models.BooleanField(null=True)

    last_sighted = models.DateTimeField(
        null=True,
    )

    colour = models.CharField(
        max_length=24,
        default='green',
    )
