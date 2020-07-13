from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register('texts', views.TextViewSet, basename='texts')

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/similar/<int:sentence_id>/', views.similar_sentences, name='similar-sentences'),
]
