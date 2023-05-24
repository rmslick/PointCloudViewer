import open3d
import os
from pcdprocessor.SceneInfo import *

## o3d.geometry.PointCloud()
def get_file_names(directory):
    file_names = []
    for file in os.listdir(directory):
        if file.endswith('.json'):
            name = os.path.splitext(file)[0]
            file_names.append(name)
    return file_names
import numpy as np
import json
session_id = None
def set_session_id(id):
    print("[INFO] ",id)
    global session_id
    session_id = id
def get_session_id():
    return session_id

class PointCloud:
    def __init__(self,id):
        self.pointcloud_id = int(id)
        self.log_api()

        #self.pointcloud = get_scene_info(get_session_id())#.point_clouds[self.pointcloud_id]
        self.scene = None
        dir = os.path.join(os.path.join(os.getcwd(),'pcdprocessor'),'user_sessions')
        fnames = get_file_names( dir )
        print(fnames)
        self.point_cloud = None
        if str(session_id) in fnames:
            print("Made it into load scenefor ",session_id)
            self.scene = Scene()
            self.scene.load_scene_from_file(str(session_id)+'.json')
            self.point_cloud = self.scene.point_clouds[str(self.pointcloud_id)]
        else:
            self.global_session = Scene(session_id)
        #return fnames
    def log_api(self):
        t = open("test.txt",'w')
        t.write(get_session_id()+'\n')
        t.close()
    def log(self,logmsg):
        t = open("test.txt",'a')
        t.write(logmsg+'\n')
        t.close()
    ''' Scene interface '''
    def set_point_cloud_points_scene(self, pointcloud):
        set_point_cloud_points(get_session_id(), self.pointcloud_id,pointcloud)
    def set_point_cloud_scene(self,pointcloud):
        set_point_cloud(get_session_id(),pointcloud,self.pointcloud_id)
    ''' Scene interface '''
    def get_center(self): 
        return self.point_cloud.get_center()
    def get_oriented_bounding_box(self,pointcloud):
        return pointcloud.get_oriented_bounding_box()

    def rotate(self,R):
        return 