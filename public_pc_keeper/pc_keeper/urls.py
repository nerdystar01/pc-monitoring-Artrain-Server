from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pc_keeper.views import PcKeeperViewSet

router = DefaultRouter()
router.register("pc_keeper", PcKeeperViewSet)

urlpatterns = [
    path("", include(router.urls)),
]