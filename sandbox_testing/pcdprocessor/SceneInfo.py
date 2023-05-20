import numpy as np
import open3d as o3d

class Scene:
    def __init__(self,session_id) -> None:
        self.session_id = session_id
        self.point_clouds = {}
        self.point_cloud_count = 0
    def add_pointcloud(self,pointcloud):
        self.point_clouds[self.point_cloud_count] = pointcloud
        self.point_cloud_count += 1