from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def create_new_scene():
    return {}

def hello(request):
    return JsonResponse({'message': 'Hello, World!'})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .sandbox import run_script
scenes = {}
@api_view(['POST'])
def sandbox(request):
    session_id = request.session.session_key
    print("Session id: ",session_id)
    if session_id not in scenes:
        scenes[session_id] = create_new_scene()
    current_scene = scenes[session_id]
    print(request.data)
    script = request.data.get('script')
    output = run_script(script)
    return Response(output)


scenes = {}

def index(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    if session_id not in scenes:
        print("New user:", session_id)
        scenes[session_id] = create_new_scene()
    current_scene = scenes[session_id]
    current_scene = scenes[session_id]
    return render(request, 'index.html')

import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def compile_code(request):
    if request.method == 'POST':
        # Get the code content from the request body
        request_json = (json.loads(request.body))
        code = request_json['code']
        # Get the user session ID
        user_session_id = request.session.session_key
        # Run the code in a subprocess and get the output
        cmd = ['python', '-c', code]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True)
            output = result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            output = e.stderr.decode('utf-8')
        except subprocess.TimeoutExpired:
            output = 'Time limit exceeded'
        except Exception as e:
            output = str(e)
        # Return the output as a JSON response
        return JsonResponse({'output': output})
