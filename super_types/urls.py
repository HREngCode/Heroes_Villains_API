from django.urls import path
from . import views
from .serializers import SuperTypeSerializer
from .models import(SuperType)

urlpatterns = [
    path('', views.super_types_list),
    path('<int:pk>', views.super_types_list),
]