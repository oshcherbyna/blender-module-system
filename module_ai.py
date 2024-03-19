'''
UTF-8
code: v1.0 by @o.shcherbyna


AI Module:
    1. Aggressive behavior tree - NPC looking for target in range to attack.
    2. Neutral behavior tree - NPC attacks only as answer to attack.

Usage:
1.  Add to Scene:
    1.1 'Neutral NPC' (Suzanne);
    1.2 'Aggressive NPC' (copy and rename of 'Neutral NPC');
    1.3 Move them to collections 'Movable'
    1.3 'Player' (rename Camera), 'Random Point' (Cube), 'Spawn Point' (Cone)
    1.4 'PlayerHpBarBack'(Plane, child of Camera) + 'HpBar' (Cube or Plane) as a child.

2.  (for module_system) Create text block main.py
    ai = import_as_module["module_ai.py"]
    ai.init() # init NPC-Templates
    game_loop():
        for npc in bpy.data.collections["Movable"]: # (you should create this coll)
            ai.update(obj) # run / update ai_logic for each object in collection every frame
'''

import bpy, time, random, math
from mathutils import Vector

print(f'[{str(__name__).upper()}] imported.')

# Debug
DEBUG = 0 # if DEBUG: print('DEBUG')
RP = bpy.context.scene.objects["Random Point"] # 'Cube' (for debug purpose)
RP.hide_viewport = True

# Player
Player = bpy.context.scene.objects["Player"]
Player["hp"] = 100

# AI Config
MAX_IDLE_TIME = 10 # how many time npc stay idle
MAX_DISTANCE = 20 # max dist to target (and spawn radius)

target_list = {} # to RandomPoints access
class Target:
    '''
    Used to create RandomPoint in BM_PATROLL mode.
    Використовується для створення RandomPoint в режимі патрулювання.
    '''
    name = 'RandomPoint'
    location = Vector((0,0,0))
    
    def  __init__(self, name):
        self.name = name

#======== Actions ============

def is_target_in_radius(obj, target, radius, z = False) -> bool:
    '''
    Squared distance check.
    Перевірка знаходження цілі в межах вказаного радіусу.
    z = True - перевіряти z-координату також
    '''
#    return (target.location - obj.location).length < radius # This is slow solution for checking a bunch of objects because of square root.
    dir = target.location - obj.location
    sq_dist = dir.x * dir.x + dir.y * dir.y # self*self works faster then math.pow(self,2)
    if z:
        sq_dist += dist.z * dist.z
    return sq_dist < radius * radius

def update_rotation(object, target, turn_speed = 0.1):
    '''
    Rotates the object around the Z-axis in the direction of the target at a speed of turn_speed.
    Обертає обʼєкт (object) навколо осі Z у напрямку цілі (target) зі швидкістю оберту turn_speed.
    '''
    # Отримуємо позицію цілі на сцені
    target_position = target.location
    
    # Отримуємо позицію та орієнтацію об'єкта
    object_position = object.location
    object_rotation = object.rotation_euler

    # Обчислюємо кут між об'єктом та ціллю
    angle = math.atan2(target_position.y - object_position.y, target_position.x - object_position.x)
    diff = object_rotation.z - angle
    
    # Визначаємо напрямок та швидкість повороту
    if (diff > math.pi): diff -= math.pi * 2
    elif (diff < -math.pi): diff += math.pi * 2
    
    impulse = 0
    impulse += diff * turn_speed
    
    object_rotation.z = angle + impulse
    object.rotation_euler = object_rotation
    
def update_position(obj, target, time = .1, speed = 1.0):
    direction = target.location - obj.location
    obj.location = obj.location + direction.normalized() * speed * time  



def is_alive(obj_name):
    return bpy.data.objects[obj_name]["hp"] > 0

#def is_enemy(obj):
#    return obj["target"] in obj["enemy_list"]


def check_idle_timer(obj):
    if time.time()-obj["start_idle_time"] < MAX_IDLE_TIME:
        if DEBUG:print('Виконую check_idle_timer(obj) - Стою чекаю таймер')
        return False
    obj["start_idle_time"] = 0
    return True

def check_weapon_timer(obj):
    if time.time()-obj["last_hit_time"] < obj["weapon_speed"]:
        if DEBUG:print('Виконую check_weapon_timer(obj) - Чекаю / перезаряджаю зброю.')
        return False # waiting for weapon
    return True # go to hit

def check_dist(obj):
    if DEBUG:print(f'\n[{obj.name}] Виконую check_dist() model = {obj["model"]}')
    
    # Check max_distance to spawn_point => if double => tele_to(spawn_point)
    sp = bpy.context.scene.objects[obj["spawn_point"]]
    radius = MAX_DISTANCE
    if not is_target_in_radius(obj, sp, radius*2, z=False): #dist > obj["weapon_range"]:
        if DEBUG:print('Я далеко від спавну. Телепортуюсь на базу.')
        obj["target"] = obj["spawn_point"]
        tele_to(obj)
        to_patroll(obj)
        return False # break actions chain

    if DEBUG:print('Ціль в межах мого поля зору.')
    return True # continue chain

def check_target(obj):
    if DEBUG:print('Виконую check_target()')
    
    if obj["player_in_radius"]: # checks by radius-driver
        if is_alive('Player'):
            obj["target"] = 'Player'
            to_attack(obj)
            return False # break current actions chain
    
    if DEBUG:print('Player далеко або мертвий - ігнорую.')
    return True
       

def check_attacker(obj):
    if DEBUG:print(f'\n[{obj.name}] Виконую check_attacker(obj) model = {obj["model"]}')

    # === TEST - Attack event by target mouse selecting ====
    if bpy.context.active_object == obj: # TODO Sets obj["target"] by Attacker for Neutral NPCs
        if is_alive('Player'):# assuming player as attacker
            if obj["player_in_radius"]: # sets by distance-driver
                obj["target"] = 'Player'
            else:
                if DEBUG:print('Ціль далеко - ігнорую.') # Target is far away, ignore it.
    # ==== END TEST ===
        
    if obj["target"] == 'Player': # TODO is_enemy(obj) and is_alive(obj["target"])
        to_attack(obj)
        return False

    if DEBUG:print('No Attackers.')
    return True

def get_target_obj(obj):
    '''
    Returns scene Object by name.
    '''
    return bpy.context.scene.objects[obj["target"]]

def get_weapon_damage(obj):
    damage = random.randint(obj["weapon_damage"][0], obj["weapon_damage"][1])
    if DEBUG:print('get_weapon_damage(obj) =', damage)
    return damage
    
def get_random_point(obj):
    ''' RandomPoint Target for Patroll behavior.'''
    if obj["target"] == str('RandomPoint-'+obj.name):
        return True # movement to RandomPoint in progress. Не визначати нові цілі поки йдемо.
    
    sp = bpy.context.scene.objects[obj["spawn_point"]]
    # New RandomPoint Target
    t = Target(str('RandomPoint-'+obj.name))
    min_x = int(sp.location.x - MAX_DISTANCE) #SPAWN_POINT_MAX_RADIUS
    max_x = int(sp.location.x + MAX_DISTANCE)
    min_y = int(sp.location.y - MAX_DISTANCE)
    max_y = int(sp.location.y + MAX_DISTANCE)
    t.location = Vector((random.randint(min_x, max_x), random.randint(min_y, max_y), sp.location.z + 0.5))
    target_list[t.name] = t
    obj["target"] = t.name
    if DEBUG:
        print(f'\n[{obj.name}] Виконую get_random_point(obj) target = {obj["target"]}')
        RP.location = t.location
        RP.hide_viewport = False
#    print(target_list)
    return True


def move_to(obj):
    if DEBUG:print('Виконую move_to()')
    if obj["target"] in bpy.data.objects:
        target = bpy.data.objects[obj["target"]] # Player
    else:
        try:
            target = target_list[obj["target"]] # RandomPointInSpawnRadius
        except KeyError: # reset target for all Movable on npc.init()
            print(f'{obj.name} init new target') # (after restart 'module_ai.py' target_list is empty)
            target = ""
            return True
    
    # Check attack distance    
    radius = obj["weapon_range"]
    if is_target_in_radius(obj, target, radius, z = False): #dist > obj["weapon_range"]:
        if DEBUG:print(f'Ціль в межах радіусу {"атаки" if obj["model"] == "BM_ATTACK" else ""}. weapon_range =', radius)#, dist) # TODO target_type = isEnemy()
        return True
    
    if DEBUG:
        if obj["model"] == 'BM_ATTACK':
            print('Дистанція для атаки завелика.')
    
    if DEBUG:print('Йду до цілі.', 'target =', obj["target"])#, 'dist =', dist)
    update_rotation(obj, target, 0.9)
    update_position(obj, target) # dist -= 2 # NPC MOVEMENT
    return False # break chain to restart it

def tele_to(obj):
    if DEBUG:print('Виконую tele_to() target =', obj["target"])
    target = bpy.data.objects[obj["target"]]
    obj.location = target.location

def hit_target(obj):
    ''' Hit action. obj hits obj["target"] '''
    print(f'[{obj.name}] Виконую hit_target() target = {obj["target"]}')
    
    target_obj = get_target_obj(obj)
    target_hp = target_obj["hp"] # Player["hp"]
    if target_hp <= 0:
        print('Ціль знищено. target_hp =', target_hp)
        if target_obj.name == 'Player':
            deselect_obj(obj) # deselect NPC
        return True
    
    print('Атакую ціль.', 'target_hp =', target_hp)
    damage = get_weapon_damage(obj)
    print(f'hit -{damage}')
    target_hp = max(target_hp - damage, 0) # do hit target
    Player["hp"] = target_hp # update target HP
    update_hp_bar()
    obj["last_hit_time"] = time.time() # save last_hit_time for the next hit delay
    return False # break chain to restart it and make a new hit
        
      
# Behavior Model Change
def to_attack(obj):
#    obj["target"] = obj["spawn_point"] # Sets by Attacker
    obj["model"] = 'BM_ATTACK'
    if DEBUG:print('Виконую to_attack() target =', obj["target"], 'model =', obj["model"])
#    return False # break chain to start new behavior model

def to_return(obj):
    obj["target"] = obj["spawn_point"]
    obj["model"] = 'BM_RETURN'
    if DEBUG:print('Виконую to_return(obj) Повертаюсь на спаун.')
    if DEBUG:print(' '*2, 'Змінюю поведінку: model =', obj["model"], ', target =', obj["target"])
    return True #  end chain

def to_patroll(obj):
    obj["target"] = "" # reset Target to get new one in get_random_point()
    obj["model"] = 'BM_PATROLL'
    if DEBUG:print('Виконую to_patroll(obj) Змінюю поведінку: model =', obj["model"])
    return True

def to_idle(obj):
    obj["target"] = "" # reset Target to get new one in get_random_point()
    obj["model"] = 'BM_IDLE'
    obj["start_idle_time"] = time.time()
    if DEBUG:print('Виконую to_idle(obj) Змінюю поведінку: model =', obj["model"])
    return True



# ==== non actions - support scripts ====

def add_distance_driver(obj, target, property, expression):
    '''
    Adds a distance-driver to the Custom property. Removes the previous one.
    '''
    obj.driver_remove(f'["{property}"]', -1) # -1 = single value
    fcurve = obj.driver_add(f'["{property}"]', -1) # https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.driver_add

    d = fcurve.driver
    d.type = "SCRIPTED"
    d.expression = expression

    v = d.variables.new()
    v.name = "var"
    v.type = 'LOC_DIFF' # https://docs.blender.org/api/current/bpy.types.DriverVariable.html

    t = v.targets[0]
    t.id = obj
    
    t = v.targets[1]
    t.id = target


def deselect_obj(obj):
    bpy.context.view_layer.objects.active = None
    obj.select_set(False)
    
def select_obj(obj):
    bpy.data.objects[obj.name].select_set(True)
    bpy.context.view_layer.objects.active = obj
        
def update_hp_bar():
    bpy.context.scene.objects["PlayerHpBarBack"].children[0].name = 'HP '+ str(Player["hp"]) + '/100'#Player["hp_max"])
    bpy.context.scene.objects["PlayerHpBarBack"].children[0].scale.x = Player["hp"] * 0.01
    # bpy.context.scene.objects["PlayerHpBarBack"].children[0].scale.y = Player["hp"] * 0.01

  
#========== TODO module_npc.init() ==============
def npc_init(obj, behav_tree, spawn_name):
    obj["ai"] = behav_tree # BT_NEUTRAL #neutral
    obj["model"] = 'BM_PATROLL'
    obj["hp"] = 100
    obj["target"] = ""
    obj["weapon_range"] = 3
    obj["weapon_speed"] = 3 # attack delay (depends on the duration of the TODO:animation)
    obj["weapon_damage"] = [10,20] # min,max
    obj["last_hit_time"] = 0
    obj["idle_timer"] = 0
    obj["spawn_point"] = spawn_name
    
    obj["player_in_radius"] = 0 # updates by Driver
    add_distance_driver(obj, Player, 'player_in_radius', f'1 if var < {MAX_DISTANCE} else 0') 
#=================


''' AI engine ==================
Updates every object in the 'Movable' collection as long as it has a behavior model set to it.
Оновлювати кожен обʼєкт в колекції "рухомих", якщо у нього встановлена модель поведінки.
'''

def get_behav_tree(id):
    return behavior_trees[id]

def run_actions(obj, functions):
    for func in functions:
        result = func(obj)

        if result == False: # break actions chain
            break

def update(obj): # ai.update(obj)
    if "model" not in obj: # avoid non movable objects
        return
    
    if obj["model"]:#while obj["model"]:
        behavior_tree = get_behav_tree(obj["ai"])
        model = obj["model"]
        actions_list = behavior_tree[model]
        if DEBUG:print('Модель:[", model, "] Дії:', str(actions_list))
        run_actions(obj, actions_list)

# Behavior Trees
neutral = {
    'BM_ATTACK': [check_dist, move_to, check_weapon_timer, hit_target, to_idle],#, to_return
    'BM_RETURN': [check_dist, check_attacker, move_to, to_patroll],
    'BM_PATROLL': [get_random_point, check_attacker, move_to, to_idle],
    'BM_IDLE': [check_attacker, check_idle_timer, to_patroll],
}
aggressive = {
    'BM_ATTACK': [check_dist, move_to, check_weapon_timer, hit_target, to_idle],
    'BM_RETURN': [check_dist, check_target, move_to, to_patroll],
    'BM_PATROLL': [get_random_point, check_target, move_to, to_idle],
    'BM_IDLE': [check_target, check_idle_timer, to_patroll],
}
behavior_trees = [neutral, aggressive]
BT_NEUTRAL = 0 # => neutral behav_tree
BT_AGGRESSIVE = 1 # => aggressive behav_tree

        
#====== TEST =======    
if __name__ == "__main__":
    
    update_hp_bar()
    
    NPC = bpy.context.scene.objects["Neutral NPC"]
    NPC_AGGRO = bpy.context.scene.objects["Aggressive NPC"]
    
    npc_init(NPC, BT_NEUTRAL, 'Spawn Point')  # init neutral character
    npc_init(NPC_AGGRO, BT_AGGRESSIVE, 'Spawn Point') # init aggressive character
    
    def game_loop(self, context):
        
        for npc in bpy.data.collections["Movable"].objects:
            update(npc)# ai.update(obj) # run behavior model every frame
        
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(game_loop)




    