from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response

from airports.models import Airport


class AirportsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Airport.objects.all()

    def get(self, request):
        content = [str(airport) for airport in self.queryset.all()]
        return Response(content)
