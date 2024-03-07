from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=360)
    
    def no_of_ratings(self):
        ratings = Ratring.objects.filter(meal=self)
        return len(ratings)
    
    def avg_ratings(self):
        sum = 0
        ratings = Ratring.objects.filter(meal=self)
        for x in ratings:
            sum += x.stars
        if len(ratings) > 0:    
            return sum / len(ratings)
        else:
            return 0
    
    def __str__(self) -> str:
        return  self.title
    
    
class Ratring(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    # def  __str__(self) -> str:
    #     return self.meal
    
    
    class Meta:
        unique_together = (('user','meal'),)
        index_together = (('user','meal'),)
        