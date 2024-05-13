from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Message
from app.serializers import MessageSerializers
from django.db.models import Q


# class MessageAPIView(generics.ListAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializers

class MessageAPIView(APIView):
    def get(self, request):
        lst = Message.objects.filter(Q(user_from__in=[1,2]) | Q(user_to__in=[1,2])).order_by('timestamp')
        return Response({'messages': MessageSerializers(lst, many=True).data})
