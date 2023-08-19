from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response

from airports.models import Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["iata", "city", "state"]

class AirportsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Airport.objects.all()

    def get(self, request):
        content = [AirportSerializer(airport).data for airport in self.queryset.all()]
        return Response(content)
