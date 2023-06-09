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
    init_global_scene(session_id)
    print(request.data)
    script = request.data.get('script')
    output = run_script(script)
    return Response(output)

def index(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    init_global_scene(session_id)
    current_scene = get_scene_info(session_id)
    # Serialize the scene object to JSON
    scene_json = json.dumps({
        'session_id': current_scene.session_id,
        'point_clouds': current_scene.point_cloud_points,
        'point_cloud_count': current_scene.point_cloud_count,
        'ambient_light': current_scene.ambient_light,
        'directional_light': current_scene.directional_light,
    })
    # Open the file in write mode and write the dictionary as JSON

    # Pass the scene JSON to the template
    context = {
        'scene_json': scene_json,
    }
    return render(request, 'index.html',context)

def rob(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    '''
        if session_id not in global_session_dict.keys():
            s = Scene(session_id)
            add_scene_info(session_id,s)
            print("New user: ",session_id)
        else:
            print("Welcome back user: ",session_id)
        current_scene = get_scene_info(session_id)
    '''
    return render(request, 'rob.html')

import open3d as o3d
@csrf_exempt
def upload_points(request):
    print("Got points!")
    if request.method == 'POST':
        # Retrieve the points data from the request
        data = json.loads(request.body)
        points = data.get('points')
        directional_light = data.get('directional_light')
        ambient_light = data.get('ambient_light')
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
        if(session_id != None):
            add_point_cloud(session_id,point_cloud)
            add_directional_light(session_id,directional_light)
            add_ambient_light(session_id,ambient_light)
        else:
            if not request.session.session_key:
                request.session.save()
            session_id = request.session.session_key
            init_global_scene(session_id)
            print("New user: ",session_id)
            add_point_cloud(session_id,point_cloud)
            add_directional_light(session_id,directional_light)
            add_ambient_light(session_id,ambient_light)
        # Return a response indicating the successful processing of the points
        return JsonResponse({'message': 'Points uploaded successfully'})

    # Return an error response for other HTTP methods
    return JsonResponse({'error': 'Invalid request method'})

import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
def parse_code(code):
    split_code = code.split('\n')
    code_string = ';'.join( split_code )
    code_string += ';'
    return code_string
@csrf_exempt
def compile_code(request):
    if request.method == 'POST':
        #with open("test2.json", "w") as json_file:
        #    json.dump(global_session_dict, json_file)
        # Get the code content from the request body
        request_json = (json.loads(request.body))
        code = request_json['code']
        # Get the user session ID
        user_session_id = request.session.session_key
        print("[INFO] Compiling for Session id: ",user_session_id)
        # Run the code in a subprocess and get the output
        code = parse_code(code)
        cmd = ['python', '-c', 'import sys;sys.path.append("./pcdprocessor/API/");from PointCloudAPI import *;set_session_id("'+ str(user_session_id) +'");'+str(code)]
        result = 1
        try:
            print(cmd)
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True)
            output = result.stdout.decode('utf-8')
            save_path = os.path.join(os.path.join('pcdprocessor', 'user_sessions' ),str(user_session_id)+'.json')
            with open(save_path, 'r') as file:
                scene_dict = json.load(file)
            return JsonResponse({'output': output,'error_code':result.returncode,'scene':scene_dict})
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
