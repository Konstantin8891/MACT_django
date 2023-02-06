from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import MuseumSerializer
from .models import Museum


class SearchView(APIView):
    def get(self, request):
        title = Museum.objects.filter(title__contains=self.request.query_params.get('q'))
        content = Museum.objects.filter(content__contains=self.request.query_params.get('q'))
        queryset = (title | content).distinct()
        serializer = MuseumSerializer(queryset, many=True)
        return Response(serializer.data)
