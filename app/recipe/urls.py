"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)
# automatically created routes for CRUD REST view.
# Depending on the funcionality implemented in viewsets,
# specific routes will be available
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewset)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
