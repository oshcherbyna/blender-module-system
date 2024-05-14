'''
UTF-8
code: v1.0 by @o.shcherbyna

Module Player - Camera RTS
    1. props init
    2. vector movement mechanics # (!need module_keyconfig.py)

Usage (in main.py):
    module_player = bpy.data.texts["module_player_camera_rts.py"].as_module()
    player = module_player.init(scene.objects['Camera'])
    
    def game_loop(self, context):
        module_player.update(player)
'''


import bpy#, math
from mathutils import Vector

def init(obj, fullscreen = False):
    '''
    Player camera rts init.
    '''
    print(f' => [{__name__}] init()')
    
    if obj.type != 'CAMERA':
        print("Error camera_rts init. [obj] should be a camera-type.")
        return None
    
    obj["moveUp"] = False
    obj["moveDown"] = False
    obj["moveRight"] = False
    obj["moveLeft"] = False
    
    obj["walk_speed"] = 5.0
    obj["run_speed"] = 10.0
    obj["move_speed"] = obj["run_speed"]
#    obj["rotation_speed"] = 5.0
    
    view_3d = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
    view_3d.spaces[0].region_3d.view_perspective = 'CAMERA' # bpy.ops.view3d.view_camera() # Activate Camera View
    view_3d.spaces[0].lock_camera = True # Lock Cam to View in "VIEW_3D"
    
    obj.location.z = 200.0
    obj.rotation_euler.x = 0.785398 # 45 grad
    obj.rotation_euler.y = 0.0
    obj.lock_location[2] = True # Lock Cam Z-location. Unlock for gravity-mode!
    obj.lock_rotation[0] = True # Lock Cam X-rotation
    obj.lock_rotation[1] = True # Lock Cam Y-rotation
    
    obj.data.clip_end = 1000 # How far away can see the camera.
    bpy.data.cameras[obj.data.name].lens = 30.0 # bpy.data.cameras["Camera.002"].name
    bpy.data.cameras[obj.data.name].passepartout_alpha = 1.0
    
    # https://docs.blender.org/manual/en/latest/advanced/app_templates.html
    bpy.context.preferences.use_preferences_save = False # Disable Auto-save preferences
    bpy.context.preferences.inputs.use_rotate_around_active = True
    bpy.context.preferences.inputs.use_auto_perspective = True
    bpy.context.preferences.inputs.use_mouse_depth_navigate = True
    
#    Fit & Fullscreen
#    https://blenderartists.org/t/how-to-make-camera-fit-viewport-in-fullscreen-mode/1408138/2
#    https://upbge.org/docs/latest/api/bpy.ops.html    
#    with bpy.context.temp_override(window=bpy.context.window_manager.windows[0], area=bpy.context.screen.areas[5], region = bpy.context.screen.areas[5].regions[0]):
    with bpy.context.temp_override(window=bpy.context.window_manager.windows[0], area=view_3d, region = view_3d.regions[0]):
        bpy.ops.view3d.view_center_camera() # Fit camera to window width. bpy.ops.view3d.view_center_camera()
        if fullscreen:
            bpy.ops.screen.screen_full_area(use_hide_panels=True) # Set to full window screen !!!Queue 1-fit => 2-fullscreen
    
    return obj

def update(obj):
#    direction = obj.matrix_world.to_3x3() @ Vector((0, 0, -1))
#    direction.z = 0.0
    if obj["moveUp"]:
        direction = obj.matrix_world.to_3x3() @ Vector((0, 0, -1))
        direction.z = 0.0
        obj.location += direction * obj["move_speed"]
    if obj["moveDown"]:
        direction = obj.matrix_world.to_3x3() @ Vector((0, 0, -1))
        direction.z = 0.0
        obj.location -= direction * obj["move_speed"]
    if obj["moveLeft"]:
        direction = obj.matrix_world.to_3x3() @ Vector((1, 0, 0))
        obj.location -= direction * obj["move_speed"]
    if obj["moveRight"]:
        direction = obj.matrix_world.to_3x3() @ Vector((1, 0, 0))
        obj.location += direction * obj["move_speed"]
        
if __name__ == "__main__":
    pass