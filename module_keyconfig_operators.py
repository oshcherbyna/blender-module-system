'''
UTF-8
code: v1.0 by @o.shcherbyna

Keyconfig operators
    1. Set WASD moving flags # (!need scene["player"] init)

Usage (in module_keyconfig.py):
    module_kop = bpy.data.texts["module_keyconfig_operators.py"].as_module()
    module_kop.init()
'''

import bpy

#player = bpy.data.objects['Cube']
player = bpy.context.scene["player"]

class MoveLeftOn(bpy.types.Operator):
    '''
    Move Left on-state
    '''
    bl_idname = "player.move_left_on"
    bl_label = "Move Left On"

    def execute(self, context):
        player["moveLeft"] = True
        print('player["moveLeft"] =', player["moveLeft"])
        return {'FINISHED'}

class MoveLeftOff(bpy.types.Operator):
    '''
    Move Left off-state
    '''
    bl_idname = "player.move_left_off"
    bl_label = "Move Left Off"

    def execute(self, context):
        player["moveLeft"] = False
        print('player["moveLeft"] =', player["moveLeft"])
        return {'FINISHED'}

class MoveRightOn(bpy.types.Operator):
    '''
    Move Right on-state
    '''
    bl_idname = "player.move_right_on"
    bl_label = "Move Right On"

    def execute(self, context):
        player["moveRight"] = True
        print('player["moveRight"] =', player["moveRight"])
        return {'FINISHED'}

class MoveRightOff(bpy.types.Operator):
    '''
    Move Right off-state
    '''
    bl_idname = "player.move_right_off"
    bl_label = "Move Right Off"

    def execute(self, context):
        player["moveRight"] = False
        print('player["moveRight"] =', player["moveRight"])
        return {'FINISHED'}

class MoveUpOn(bpy.types.Operator):
    '''
    Move Up/Forward on-state
    '''
    bl_idname = "player.move_up_on"
    bl_label = "Move Up On"

    def execute(self, context):
        player["moveUp"] = True
        print('player["moveUp"] =', player["moveUp"])
        return {'FINISHED'}

class MoveUpOff(bpy.types.Operator):
    '''
    Move Up/Forward off-state
    '''
    bl_idname = "player.move_up_off"
    bl_label = "Move Up Off"

    def execute(self, context):
        player["moveUp"] = False
        print('player["moveUp"] =', player["moveUp"])
        return {'FINISHED'} 

class MoveDownOn(bpy.types.Operator):
    '''
    Move Down/Back on-state
    '''
    bl_idname = "player.move_down_on"
    bl_label = "Move Down On"

    def execute(self, context):
        player["moveDown"] = True
        print('player["moveDown"] =', player["moveDown"])
        return {'FINISHED'}

class MoveDownOff(bpy.types.Operator):
    '''
    Move Down/Back off-state
    '''
    bl_idname = "player.move_down_off"
    bl_label = "Move Down Off"

    def execute(self, context):
        player["moveDown"] = False
        print('player["moveDown"] =', player["moveDown"])
        return {'FINISHED'}

cls = [
    MoveLeftOn, MoveLeftOff,
    MoveRightOn, MoveRightOff,
    MoveUpOn, MoveUpOff,
    MoveDownOn, MoveDownOff,
]

def register():
    print(f'..register operators: {[cl.bl_label for cl in cls]}')
    for cl in cls:
        bpy.utils.register_class(cl)

def unregister():
    print('..unregister operators')
    for cl in cls:
        bpy.utils.unregister_class(cl)

def init():
    print(f' => [{__name__}] init()')
    try:
        unregister()
    except:
        pass  
    register()
    
    
if __name__ == "__main__":
    init()

