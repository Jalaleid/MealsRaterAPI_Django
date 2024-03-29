from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import MealViewSet,RatingViewSet,UserViewSet


router = routers.DefaultRouter()
router.register('user',UserViewSet)
router.register('meals',MealViewSet)
router.register('ratings',RatingViewSet)

urlpatterns = [
    path("", include(router.urls))
    
]
