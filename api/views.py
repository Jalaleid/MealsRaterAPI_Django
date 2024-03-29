from .serializers import MealSerializer,RatingSerializer,UserSerializer
from .models import Meal,Ratring

#django
from django.http import request
from django.contrib.auth.models import User

#rest framework
from rest_framework import viewsets,status 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        print(created)
        
        return Response({'token':token.key},status=status.HTTP_201_CREATED)
    
    


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @action(methods=['POST'],detail=True)
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            '''
                Create OR Updates
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                # Update
                rating = Ratring.objects.get(user=user.id, meal=meal.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating,many=False)
                json = {
                    'message':'Meal Rate Updated',
                    'result':serializer.data
                }
                return Response(json,status=status.HTTP_202_ACCEPTED)
            except:
                # Create
                rating = Ratring.objects.create(user=user,meal=meal,stars = stars)
                serializer = RatingSerializer(rating,many=False)
                json = {
                    'message':'Meal Rate Created',
                    'result':serializer.data
                }
                return Response(json,status=status.HTTP_201_CREATED)
                
        
        else:
            json = {
                    'message':'stars not provided'
                }
            return Response(json,status=status.HTTP_400_BAD_REQUEST)
            


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Ratring.objects.all()
    serializer_class = RatingSerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        response  = {'message':'Invalid wat to update'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response  = {'message':'Invalid wat to ceate'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
