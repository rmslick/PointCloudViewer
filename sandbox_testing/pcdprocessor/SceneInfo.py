import numpy as np
import open3d as o3d

class Scene:
    def __init__(self,session_id):
        #point clouds
        self.session_id = session_id
        self.point_clouds = {}
        self.point_cloud_points = {}
        self.point_cloud_count = 0
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

    def add_pointcloud(self,pointcloud):
        self.point_clouds[self.point_cloud_count] = pointcloud
        points_list = np.asarray(pointcloud.points).tolist()
        self.point_cloud_points[self.point_cloud_count] = points_list
        self.point_cloud_count += 1
        print("[INFO] Point cloud added.")
    def add_ambient_light(self,ambient_light):
        print("[INFO] Ambient light set.")
        self.ambient_light['color'] = hex(ambient_light['color'])
        self.ambient_light['intensity'] = ambient_light['intensity']
        
    def add_directional_light(self,directional_light):
        print("[INFO] Directional light set.")
        self.directional_light['color'] = hex(directional_light['color'])
        self.directional_light['intensity'] = directional_light['intensity']
