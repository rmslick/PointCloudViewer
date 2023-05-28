import numpy as np
import open3d as o3d
import json
import os

class Scene:
    def __init__(self,session_id=None):
        # default constructur for load from file
        # load current sessions
        if session_id == None:
            self.session_id = None
            self.point_clouds = {}
            self.point_cloud_points = {}
            self.point_cloud_count = 0
            self.ambient_light = {'color':0,'intensity':0}
        else:
            #point clouds
            self.session_id = session_id
            self.point_clouds = {}
            self.point_cloud_points = {}
            self.point_cloud_count = 0
            self.directional_light = {'color':0,'intensity':0}
            # lighting
            '''
                Ambient light is a non-directional light that uniformly illuminates all objects in the scene, simulating indirect or global illumination

                color (optional): This argument represents the color of the ambient light. It can be specified in various formats, such as a hexadecimal color code (0xffffff), an RGB value (rgb(255, 255, 255)), or a Three.js Color instance (new THREE.Color(1, 1, 1)). If not provided, the default value is white (0xffffff).
                intensity (optional): This argument represents the intensity or brightness of the ambient light. It is a numeric value ranging from 0 to positive infinity. Higher intensity values make the light brighter, while lower values make it dimmer. The default value is 1, which represents full intensity.
            '''
            self.ambient_light = {'color':0,'intensity':0}
            '''
                THREE.DirectionalLight is a class representing a directional light source in a 3D scene. A directional light emits light in a specific direction from an infinitely far distance, as if it is coming from an infinitely large source. This type of light simulates the effect of sunlight in a scene, where all rays of light are parallel.
                The THREE.DirectionalLight constructor takes the following arguments:

                color (optional): This argument represents the color of the directional light. It can be specified in various formats, such as a hexadecimal color code (0xffffff), an RGB value (rgb(255, 255, 255)), or a Three.js Color instance (new THREE.Color(1, 1, 1)). If not provided, the default value is white (0xffffff).
                intensity (optional): This argument represents the intensity or brightness of the directional light. It is a numeric value ranging from 0 to positive infinity. Higher intensity values make the light brighter, while lower values make it dimmer. The default value is 1, which represents full intensity.
            '''
            self.directional_light = {'color':0,'intensity':0}
            self.save_scene_to_file()
    def add_pointcloud(self,pointcloud):
        self.point_clouds[self.point_cloud_count] = pointcloud
        points_list = np.asarray(pointcloud.points).tolist()
        self.point_cloud_points[self.point_cloud_count] = points_list
        self.point_cloud_count += 1
        self.save_scene_to_file()
        print("[INFO] Point cloud added.")
    def add_ambient_light(self,ambient_light):
        print("[INFO] Ambient light set.")
        self.ambient_light['color'] = hex(ambient_light['color'])
        self.ambient_light['intensity'] = ambient_light['intensity']
        self.save_scene_to_file()
    def add_directional_light(self,directional_light):
        print("[INFO] Directional light set.")
        self.directional_light['color'] = hex(directional_light['color'])
        self.directional_light['intensity'] = directional_light['intensity']
        self.save_scene_to_file()
    
    def save_scene_to_file(self):
        filename = str( self.session_id )+".json"
        scene_dict = {
            'session_id': self.session_id,
            'point_clouds': {},  # Initialize an empty dictionary
            'point_cloud_points': self.point_cloud_points,
            'point_cloud_count': self.point_cloud_count,
            'ambient_light': self.ambient_light,
            'directional_light': self.directional_light
        }

        # Convert point clouds to NumPy arrays
        for key, point_cloud in self.point_clouds.items():
            points_array = np.asarray(point_cloud.points)
            scene_dict['point_clouds'][key] = points_array.tolist()
        # Convert point clouds to NumPy arrays
        for key, point_cloud in self.point_cloud_points.items():
            scene_dict['point_cloud_points'][key] = points_array.tolist()
        pcdprocessorpath = os.path.join(os.getcwd(),'pcdprocessor')
        save_path = os.path.join(os.path.join(pcdprocessorpath,'user_sessions'),filename)
        with open(save_path, 'w') as file:
            json.dump(scene_dict, file)
        # change to the scene has been made, notify the user
        
    def load_scene_from_file(self,filename):
        filename = str( filename )
        pcdprocessorpath = os.path.join(os.getcwd(),'pcdprocessor')
        save_path = os.path.join(os.path.join(pcdprocessorpath,'user_sessions'),filename)
        print("Reading: ",save_path)
        with open(save_path, 'r') as file:
            scene_dict = json.load(file)

        self.session_id = scene_dict['session_id']
        point_clouds = {}
        point_cloud_points = scene_dict['point_cloud_points']
        point_cloud_count = scene_dict['point_cloud_count']
        ambient_light = scene_dict['ambient_light']
        directional_light = scene_dict['directional_light']

        for key, points_list in scene_dict['point_clouds'].items():
            points_array = np.asarray(points_list)
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(points_array)
            point_clouds[key] = point_cloud
        #print(point_clouds.keys(),type(list(point_clouds.keys())[0]))
        #scene = Scene(session_id)
        self.point_clouds = point_clouds
        self.point_cloud_points = point_cloud_points
        self.point_cloud_count = point_cloud_count
        self.ambient_light = ambient_light
        self.directional_light = directional_light
        