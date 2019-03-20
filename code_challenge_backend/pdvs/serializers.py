from rest_framework import serializers
from .models import Pdv


class PdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdv
        fields = '__all__'
