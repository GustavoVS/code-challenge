from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Pdv(models.Model):

    trading_name = models.CharField(_('Trading Name'), max_length=255)
    owner_name = models.CharField(_('Owner Name'), max_length=100)
    document = models.CharField(_('Document'), unique=True, max_length=34)
    coverage_area = models.MultiPolygonField(srid=4326)
    address = models.PointField(srid=4326)

    class Meta:
        verbose_name = _("PDV")
        verbose_name_plural = _("PDVs")

    def __unicode__(self):
        return self.titleasasd

    def get_absolute_url(self):
        return reverse("PDV_detail", kwargs={"pk": self.pk})
