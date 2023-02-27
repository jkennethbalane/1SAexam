from django.db import models

class parkingFee(models.Model):
    mode = models.CharField(max_length=100)
    fee = models.IntegerField()
    succeedingFee = models.IntegerField()

    def __str__(self):
        return self.mode
