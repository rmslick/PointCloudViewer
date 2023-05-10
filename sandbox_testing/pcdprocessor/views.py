from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def hello(request):
    return JsonResponse({'message': 'Hello, World!'})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .sandbox import run_script

@api_view(['POST'])
def sandbox(request):
    print(request.data)
    script = request.data.get('script')
    output = run_script(script)
    return Response(output)