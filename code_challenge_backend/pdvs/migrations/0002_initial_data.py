
import os
import json
import re
from django.db import migrations
from pdvs.serializers import PdvSerializer
from django.conf import settings


def camel2snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def import_pdvs_from_json(apps, schema_editor):

    with open(os.path.join(settings.BASE_DIR, 'pdvs', 'files', 'pdvs.json')) as pdvs_file:
        pdvs_json = json.load(pdvs_file)
        
        for pdv_json in pdvs_json['pdvs']:
            
            for field in pdv_json:
                pdv_json[camel2snake(field)] = pdv_json.pop(field)
            
            pdv = PdvSerializer(data=pdv_json)

            if pdv.is_valid():
                pdv.save()

        pdvs_file.close()


class Migration(migrations.Migration):

    dependencies = [
        ('pdvs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_pdvs_from_json)
    ]

