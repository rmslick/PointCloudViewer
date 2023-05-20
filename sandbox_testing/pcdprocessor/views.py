from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np

def create_new_scene():
    return {}

def hello(request):
    return JsonResponse({'message': 'Hello, World!'})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .sandbox import run_script
from pcdprocessor.SceneInfo import *
from pcdprocessor.global_session_dict import * 

scenes = {}
@api_view(['POST'])
def sandbox(request):
    session_id = request.session.session_key
    print("Session id: ",session_id)
    if session_id not in global_session_dict.keys():
        s = Scene(session_id)
        add_scene_info(session_id,s)
    current_scene = get_scene_info(session_id)
    print(request.data)
    script = request.data.get('script')
    output = run_script(script)
    return Response(output)



def index(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    if session_id not in global_session_dict.keys():
        s = Scene(session_id)
        add_scene_info(session_id,s)
        print("New user: ",session_id)
    else:
        print("Welcome back user: ",session_id)
    current_scene = get_scene_info(session_id)
    return render(request, 'index.html')

def rob(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    if session_id not in global_session_dict.keys():
        s = Scene(session_id)
        add_scene_info(session_id,s)
        print("New user: ",session_id)
    else:
        print("Welcome back user: ",session_id)
    current_scene = get_scene_info(session_id)
    return render(request, 'rob.html')

import open3d as o3d
@csrf_exempt
def upload_points(request):
    print("Got points!")
    if request.method == 'POST':
        # Retrieve the points data from the request
        data = json.loads(request.body)
        points = data.get('points')
        print(points)
        # Process the points data and load into Open3D point cloud
        # Convert the points data to a numpy array
        points_np = np.array(points, dtype=np.float32)

        # Reshape the array to Nx3 shape
        points_np = points_np.reshape(-1, 3)

        # Create an Open3D point cloud from the numpy array
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points_np)
        session_id = request.session.session_key
        add_point_cloud(session_id,point_cloud)

        # Perform any additional operations on the point cloud as needed
        # ...

        # Return a response indicating the successful processing of the points
        return JsonResponse({'message': 'Points uploaded successfully'})

    # Return an error response for other HTTP methods
    return JsonResponse({'error': 'Invalid request method'})

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
        result = 1
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True)
            output = result.stdout.decode('utf-8')
            return JsonResponse({'output': output,'error_code':result.returncode})
        except subprocess.CalledProcessError as e:
            output = e.stderr.decode('utf-8')
            return JsonResponse({'output': output,'error_code':result})
        except subprocess.TimeoutExpired:
            output = 'Time limit exceeded'
            return JsonResponse({'output': output,'error_code':result})
        except Exception as e:
            output = str(e)
        # Return the output as a JSON response
            return JsonResponse({'output': output,'error_code':result})
