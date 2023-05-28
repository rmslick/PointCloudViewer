# global_dict.py
import numpy as np
import os
from pcdprocessor.SceneInfo import *
import open3d
global_session = None
def get_file_names(directory):
    file_names = []
    for file in os.listdir(directory):
        if file.endswith('.json'):
            name = os.path.splitext(file)[0]
            file_names.append(name)
    return file_names

def init_global_scene(session_id):
    global global_session
    dir = os.path.join(os.path.join(os.getcwd(),'pcdprocessor'),'user_sessions')
    fnames = get_file_names( dir )
    #print(fnames)
    if str(session_id) in fnames:
        return Scene().load_scene_from_file(str(session_id)+'.json')
        
    else:
        global_session = Scene(session_id)
        return fnames

def get_scene_info(session_id):
    global global_session
    return global_session
def add_point_cloud(session_id,point_cloud):
    #global global_session_dict
    global_session.add_pointcloud(point_cloud)
def add_ambient_light(session_id,ambient_light):
    global_session.add_ambient_light(ambient_light)
def add_directional_light(session_id,directional_light):
    global_session.add_directional_light(directional_light)
def set_point_cloud_points(session_id,pointcloud_id,pointcloud):
    global_session.point_cloud_points[pointcloud_id] = np.asarray(pointcloud.points).tolist()
def set_point_cloud(session_id,pointcloud,id):
    global_session.pointclouds[id] = pointcloud
        
def get_point_cloud(pid):
    return  open3d.utility.Vector3dVector( np.asarray( global_session.point_clouds[pid] ) )