from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# /api/recipe/tags/1
# This registers our viewset with our router
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
