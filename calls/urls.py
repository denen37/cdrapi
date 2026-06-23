from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"calls", views.CallViewSet)

urlpatterns = [
     path("", include(router.urls)),
     # path("", views.getData, name="get_all_calls"),
]