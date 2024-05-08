'''
UTF-8
code: v1.0 by @o.shcherbyna

Module Player
    1. props init
    2. vector movement mechanics # (!need module_keyconfig.py)

Usage (in main.py):
    module_player = bpy.data.texts["module_player.py"].as_module()
    player = module_player.init(scene.objects['Rocket Launcher'])
    
    def game_loop(self, context):
        module_player.update(player)
'''


import bpy, math
from mathutils import Vector

def get_forward_vector(obj):  
    local_vec = Vector((0.0, 1.0, 0.0))
    if obj.type == 'CAMERA':
#        print("obj.type == 'CAMERA'")
        local_vec = Vector((0.0, 0.0, -1.0))
    
    return obj.matrix_world.to_quaternion() @ local_vec #).normalized()

def move_forward(obj, speed):
    # Отримуємо кадрову частоту сцени
    fps = bpy.context.scene.render.fps
    
    # Отримуємо час між кадрами (в секундах)
    frame_time = fps ** -1 #1.0 / fps #need perfom. test
    
    # Отримуємо напрямок вперед в глобальній системі координат
    forward_vector = get_forward_vector(obj) #obj.matrix_world.to_quaternion() @ Vector((0.0, 1.0, 0.0))
    
    # Визначаємо вектор зсуву шляхом множення forward-вектора на швидкість та час
    displacement = forward_vector * (speed * frame_time)
    
    # Змінюємо позицію об'єкта на вектор зсуву
    obj.location += displacement

def rotate_z(obj, angular_speed):
    # Отримуємо поточний кут обертання по осі Z
    current_rotation_z = obj.rotation_euler.z
    
    # Обчислюємо новий кут обертання, додаючи швидкість оберту
    new_rotation_z = current_rotation_z + math.radians(angular_speed)
    
    # Задаємо новий кут обертання об'єкту
    obj.rotation_euler.z = new_rotation_z

def init(obj):
    '''
    Player object props init.
    '''
    print(f' => [{__name__}] init()')
    obj["moveUp"] = False
    obj["moveDown"] = False
    obj["moveRight"] = False
    obj["moveLeft"] = False
    
    obj["walk_speed"] = 5.0
    obj["run_speed"] = 10.0
    obj["move_speed"] = obj["walk_speed"]
    obj["rotation_speed"] = 5.0
    return obj
    
def update(obj):
    '''
    Player object update.
    '''
    if obj["moveUp"]:
        move_forward(obj, obj["move_speed"])
    if obj["moveDown"]:
        move_forward(obj, -obj["move_speed"])
    if obj["moveRight"]:
        rotate_z(obj, -obj["rotation_speed"])
    if obj["moveLeft"]:
        rotate_z(obj, obj["rotation_speed"])

if __name__ == "__main__":
    pass
#    print(get_forward_vector(bpy.data.objects['Camera']))