from django.urls import include, path

from rest_framework import routers

from .views import TagViewSet, RecipeViewSet, IngredientViewSet

app_name = 'api'

router_number1 = routers.DefaultRouter()

router_number1.register(
    'tags',
    TagViewSet,
    basename='tags'
)
router_number1.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router_number1.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)

urlpatterns = [
    path('v1/', include(router_number1.urls)),
]
