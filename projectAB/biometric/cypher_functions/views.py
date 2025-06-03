from django.shortcuts import render
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def receive_data(request):
    data = request.data
    print("Received from ESP32:", data)
    return Response({"status": "Data received"})
