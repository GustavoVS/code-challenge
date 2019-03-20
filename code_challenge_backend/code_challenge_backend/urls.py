from django.urls import include, path
from rest_framework import routers
from pdvs.views import PdvViewSet, SearchPdvAPIView


router = routers.DefaultRouter()
router.register(r'pdv', PdvViewSet, base_name='pdv')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/search-pdv/', SearchPdvAPIView.as_view(), name="search-pdv")
]
