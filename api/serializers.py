from .models import Meal,Ratring

from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {'password':{'write_only':True,'required':True}}

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id','title','description','no_of_ratings','avg_ratings')

        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratring
        fields = ('id','stars','user', 'meal')