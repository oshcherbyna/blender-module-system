'''
UTF-8
code: v1.0 by @o.shcherbyna

Module Animations
Contains a list of NLA/action animations and functions to work with.
You have to prepare your animations first:
    https://blenderartists.org/t/bege-module-animations-devlog

# Usage:
m_anim = bpy.data.texts["module_animations.py"].as_module()
m_anim.nla_play("Armature_Name", "Idle")
m_anim.nla_play("Player", "Impact", rand=True, delay = 0.5)
m_anim.nla_play("Player", "Attack", rand=True)
m_anim.nla_play("Player", "Run")
'''

import bpy
import random

import functools

DEBUG = 0
FPS = bpy.context.scene.render.fps

def add_timer(callback, *args, delay:float = 0.0):
    '''
        Adds a new timer call.
    '''
    try: bpy.app.timers.unregister(callback)
    except: pass
    bpy.app.timers.register(functools.partial(callback, *args), first_interval=delay)

#====== Simple Action animation =====

def get_anim(obj_name):
    '''Get anim from Empty => Armature => animation_data '''
    return bpy.data.objects[obj_name].children[0].animation_data.action
#    return bpy.data.objects[Empty].children['Lizardman'].animation_data.action

def set_anim(obj_name, anim_id:str):
    '''Set anim to Empty => Armature => animation_data '''
    if anim_id not in animations.keys():
        print(f'ERROR: set_anim() > "{anim_id}". Use "IDLE" | "WALK" | "RUN" | "ATTACK" | "DIE"')
        return
    if animations[anim_id] == "":
        print(f'ERROR: [module_animations] > set_anim() > Animation "{anim_id}" not found!')
        return 

    anim_name = animations[anim_id]
    if obj_name == 'Player': # Armature
        bpy.data.objects[obj_name].animation_data.action = bpy.data.actions[anim_name]
    else: # Empty.Armature
        bpy.data.objects[obj_name].children[0].animation_data.action = bpy.data.actions[anim_name]
    
animations = {
    "IDLE": "Unarmed Idle",
    "WALK": "Standing Walk Forward",
    "RUN": "",
    "HIT": "Standing Melee Attack Downward",
    "WAIT": "Standing Idle",
    "DEATH": "",
    "MFighter_IDLE": "MFighter_Unarmed Idle",
    "MFighter_DEATH": "MFighter Death3",
    "MFighter_COMBAT": "MFighter Combat",
    "MFighter_RUN": "MFighter Run",
    "MFighter_IMPACT": random.choice(["MFighter Impact", "MFighter Impact2"])
}
#set_anim('Player', 'MFighter_IMPACT')
#set_anim(obj.name, 'WALK')

#====== NLA ======

def get_nla_state(armature_name:str):
    '''Tool. Returns mute-state all nla-tracks of obj'''
    track_name = 'ALL_MUTED'
    state = []
    for track in bpy.data.objects[armature_name].animation_data.nla_tracks[:]:
        state.append(int(track.mute))
        if track.mute == False:
            track_name = track.name
    return {track_name: state}

#print(get_nla_state("Player"))
#print('Run' in str(get_nla_state("Lizardman").keys())) # False
#print([key for key in get_nla_state('Lizardman').keys()][-1]) # Lizard Walk Loop

#nla_tracks = {"NLA Track names": [nla_tracks mute-states]}
#npc_nla = {
#    'Lizard Death Pose':    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],# => id[9] = 1022
#    'Lizard Death':         [1, 1, 1, 1, 1, 1, 0, 1, 0, 1],# => id[8] = 1013
#    'Lizard Attack1':       [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],# => id[7] = 1011
#    'Lizard Combat Loop':   [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],# => id[6] = 1015
#    'Lizard Combat':        [0, 1, 1, 1, 1, 0, 1, 1, 1, 1],# => id[5] = 495
#    'Lizard Run Loop':      [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],# => id[4] = 991
#    'Lizard Run':           [0, 1, 1, 0, 1, 1, 1, 1, 1, 1],# => id[3] = 447
#    'Lizard Walk Loop':     [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],# => id[2] = 895
#    'Lizard Walk':          [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],# => id[1] = 255
#    'Lizard Idle Loop':     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1] # => id[0] = 511
#}
#print(int(''.join(map(str, [0, 0, 1, 1, 1, 1, 1, 1, 1, 1])), 2))
#npc = [511, 255, 895, 447, 991, 495, 1015, 1011, 1013, 1022]

#print(int(''.join(map(str, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])), 2))
#'Player': [1023, 511, 1791, 895, 959, 1951, 1967, 951, 955, 2045, 2046],

nla = {
    'Player':       [1023, 511, 1791, 895, 959, 1951, 1967, 951, 955, 2045, 2046],
    'Lizardman':    [511, 255, 895, 447, 991, 495, 1015, 1011, 1013, 1022],
    'Lizardman*':   [511, 255, 895, 447, 991, 495, 1015, 1011, 1013, 1022],
}

def get_track_name_by_id(armature_name:str, nla_track_id:int):
    return bpy.data.objects[armature_name].animation_data.nla_tracks[nla_track_id].name

def get_track_id_by_name(armature_name:str, nla_track_name:str):
    '''Returns nla_track index by name or -1 if track not found.'''
    return bpy.data.objects[armature_name].animation_data.nla_tracks.find(nla_track_name)
    
def get_track_ids_by_keyword(armature_name:str, keyword:str):
    '''Returns a list of nla_track_ids [0..n] which contain the searched keyword in their names.'''
    ids = [] # id = -1
    for i, track in enumerate(bpy.data.objects[armature_name].animation_data.nla_tracks):
        if keyword in track.name:
            ids.append(i) # id = i
#            print(f'get_track_id_by_keyword()> Search for: "{keyword}" Result: [{i}] - {track.name}.')
    return ids # id

#(b>>0)&1 # get bit value (from right min bit 0001 to=> left max bit 1000)
def nla_set(armature_name:str, nla_track_id:int):
    '''
    Set mute-value to all tracks according to given id.
    nla_track_id = 0..n
    '''
    # Save current anim id to obj-prop
    if bpy.data.objects[armature_name].parent is None:
        bpy.data.objects[armature_name]["nla_track_id"] = nla_track_id # Player
    else:
        bpy.data.objects[armature_name].parent["nla_track_id"] = nla_track_id # NPC/'Empty'/obj["nla_track_id"]
    
    nla_key = armature_name.split('.')[0] # lizard.001 => lizard
    nla_val = nla[nla_key] # [511, 255, 895, 447, 991, 495, 1015, 1011, 1013, 1022],

    for i in range(len(nla_val)): # len(nla_val) => tracks number => walk through all nla_tracks[0-9]
        bpy.data.objects[armature_name].animation_data.nla_tracks[i].mute = (nla_val[nla_track_id] >> (len(nla_val)-1)-i) & 1 # set mute state by coresponding bit value
#        print(i, (nla_val[id] >> (len(nla_val)-1)-i) & 1)

#nla_set('Lizardman', 0)
#nla_set('Player', 10)


def nla_set_now(armature_name:str, nla_track_id:int, rand = False):#set_nla_state_now
    '''
    Sets mute-states. Moves Strip to the current_frame.
    '''
    nla_set(armature_name, nla_track_id) #set_nla_state
    bpy.data.objects[armature_name].animation_data.nla_tracks[nla_track_id].strips[0].frame_start_ui = bpy.context.scene.frame_current
    if rand:
        bpy.data.objects[armature_name].animation_data.nla_tracks[nla_track_id].strips[0].use_reverse = random.choice([0, 1])  
    
    
def on_anim_end(armature_name:str, nla_track_id:int):
    '''
    Sets mute-states after finishing of prev animation strip.
    '''
    nla_set(armature_name, nla_track_id)
    return None

def on_frame_0(armature_name:str, nla_key:str): # nla{ nla_key: [..] }
    '''
    Repeats play attempt when current_frame = 0.
    '''
    nla_play(armature_name, nla_key)
    return None

def get_strip_length(armature_name:str, nla_track_id:int):
    return bpy.data.objects[armature_name].animation_data.nla_tracks[nla_track_id].strips[0].frame_end_ui - bpy.data.objects[armature_name].animation_data.nla_tracks[nla_track_id].strips[0].frame_start_ui

def get_nla_speed(armature_name:str, nla_track_name:str, weapon_delay:float = 1.0): # TO rename => get_nla_duration ..
    '''
    Animation speed. Lower scale => shorter strip => faster animation.
    Sets nla_clip.scale. Returns anim_duration|strip_length based on weapon_delay for ai.weapon_recharge & hit timer
    '''
    bpy.data.objects[armature_name].animation_data.nla_tracks[nla_track_name].strips[0].scale = weapon_delay
    return get_strip_length(armature_name, nla_track_name) * 0.1 # 60 => 6 => weapon recharge (waiting) time
        
def nla_play(armature_name:str, nla_keyword:str, rand:bool = False, delay:float = 0.0):
    '''
        Checks conditions, performs anim.
        nla_keyword: 'Attack'/'Run'/'Idle'..
    '''
    # Get nla_track names that contain a given keyword (nla_tracks_key => nla_tracks{}).
    ids_list = get_track_ids_by_keyword(armature_name, nla_keyword) # "Run" => [3, 4] 'MFighter Run', 'MFighter Run Loop'
    
    if len(ids_list) == 0:
        print(f'{nla_keyword} not found in nla_tracks => return')
        return
    
    if rand:
        if DEBUG: print(f'Play random: {random.choice(ids_list)}') # ['Impact1', 'Impact2'] or ['Attack']
        if DEBUG: print('add_timer(ON_DELAY)')
        add_timer(nla_set_now, armature_name, random.choice(ids_list), rand, delay = delay)
        return
    
    if len(ids_list) == 1:
        if DEBUG: print(f'Play 1 key: {armature_name} - {ids_list[0]}') # 'Idle'
        nla_set(armature_name, ids_list[0])
        return
    
    # play 2-tracks sequence (blend_in => loop)
    if DEBUG: print(f'Play sequence: {ids_list}') # [3, 4] 'MFighter Run', 'MFighter Run Loop'
    clip_end = bpy.data.objects[armature_name].animation_data.nla_tracks[ids_list[0]].strips[0].action_frame_end
    
    # check if there are enough frames to play the strip, otherwise wait for frame 0
    if (bpy.context.scene.frame_current + clip_end) < bpy.context.scene.frame_end:
        nla_set_now(armature_name, ids_list[0]) # 'MFighter Run'
        if DEBUG: print('add_timer(ON_ANIM_END)')
        add_timer(on_anim_end, armature_name, ids_list[1], delay = clip_end/FPS) # 'MFighter Run Loop'
    else:
        if DEBUG: print('add_timer(ON_FRAME_0)') # wait for frame 0 and repeat attempt
        add_timer(on_frame_0, armature_name, nla_keyword, delay = (bpy.context.scene.frame_end - bpy.context.scene.frame_current)/FPS)


    


if __name__ == "__main__":
    pass
#    nla_play("Player", "Idle")
#    nla_play("Player", "Impact", rand=True, delay = 0.5)
#    nla_play("Player", "Attack", rand=True)
#    nla_play("Player", "Run")
#    nla_play("Lizardman*", "Run")
#    nla_play("Player", "Combat")
#    nla_play("Player", "Death")
#    obj = bpy.data.objects['Empty*']
#    print(obj.children[0].name)
#    nla_play(obj.children[0].name,'Attack', rand=True)