from django.db import models

# Create your models here.


class Odd(models.Model):
    team_name = models.CharField(max_length=200, null=True, blank=True)
    time = models.CharField(max_length=200, null=True, blank=True)
    score = models.CharField(max_length=200, null=True, blank=True)
    odd_1 = models.CharField(max_length=200, null=True, blank=True)
    odd_x = models.CharField(max_length=200, null=True, blank=True)
    odd_2 = models.CharField(max_length=200, null=True, blank=True)
    opening_odd = models.CharField(max_length=200, null=True, blank=True)
    payout = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.team_name)
