from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class humans(models.Model):
    part = models.IntegerField()
    round = models.IntegerField()
    PlayerOne = models.IntegerField(validators=[MaxValueValidator(3),MinValueValidator(1)])
    PlayerTwo = models.IntegerField(validators=[MaxValueValidator(3),MinValueValidator(1)])

class humansRobot(models.Model):
     game = models.IntegerField()
     round = models.IntegerField()
     opponent = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)])
     agent = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)])
     Model_Used = models.CharField(max_length=15)
     System = models.CharField(max_length=15)
     Pseudo_player = models.CharField(max_length=15)
     Gain = models.FloatField(validators=[MaxValueValidator(200.0), MinValueValidator(0.0)])
