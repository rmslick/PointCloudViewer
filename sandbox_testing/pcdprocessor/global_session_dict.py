# global_dict.py

global_session_dict = {}

def add_scene_info(session_id, scene_info):
    global_session_dict[session_id] = scene_info

def get_scene_info(session_id):
    return global_session_dict.get(session_id)