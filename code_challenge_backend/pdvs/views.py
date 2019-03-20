from rest_framework import viewsets, generics
from django.contrib.gis.geos import GEOSGeometry
from django.http import Http404
from .models import Pdv
from .serializers import PdvSerializer


class PdvViewSet(viewsets.ModelViewSet):
    queryset = Pdv.objects.all()
    serializer_class = PdvSerializer


class SearchPdvAPIView(generics.RetrieveAPIView):
    serializer_class = PdvSerializer

    def get_object(self):
        lng = self.request.query_params.get('lng')
        lat = self.request.query_params.get('lat')
        point = GEOSGeometry('POINT({} {})'.format(lng, lat), srid=4326)

        pdvs = Pdv.objects.filter(coverage_area__contains=point)
        if not pdvs:
            raise Http404
        elif pdvs.count() > 1:
            pdv = sorted(pdvs, key=lambda p: p.address.distance(point))
            return pdv[0]
        else:
            return pdvs[0]
