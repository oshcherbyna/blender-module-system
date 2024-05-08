'''
Module Keyconfig
    1. Binding keyboard keys to keyconfig_operators

Usage (in main.py):
    module_keyconfig = bpy.data.texts["module_keyconfig.py"].as_module()
    module_keyconfig.init()
'''

import bpy

module_kop = bpy.data.texts["module_keyconfig_operators.py"].as_module()
module_kop.init()

addon_keymaps = []

game_keys = { # keymap_item.type: keymap_item.idname, .type, .value
        'Move Up On': ('3D View', 'player.move_up_on', 'W', 'PRESS'), # WASD-Moving
        'Move Up Off': ('3D View', 'player.move_up_off', 'W', 'RELEASE'),
        'Move Down On': ('Object Mode', 'player.move_down_on', 'S', 'PRESS'),
        'Move Down Off': ('Object Mode', 'player.move_down_off', 'S', 'RELEASE'),
        'Move Left On': ('Object Mode', 'player.move_left_on', 'A', 'PRESS'),
        'Move Left Off': ('Object Mode', 'player.move_left_off', 'A', 'RELEASE'),
        'Move Right On': ('3D View', 'player.move_right_on', 'D', 'PRESS'),
        'Move Right Off': ('3D View', 'player.move_right_off', 'D', 'RELEASE'),
}
   
def register():

    # Add a shortcut 
    # https://blender.stackexchange.com/questions/178959/enable-disable-3d-cursor-tool-properties-from-python
    wm = bpy.context.window_manager
#    kc = wm.keyconfigs.addon
#    if not kc: return # if kc:
    
    # Cleaning
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    for key in game_keys:
        kmi_found = False
        km_name = game_keys[key][0]
        if km_name in wm.keyconfigs.addon.keymaps:
            for kmi in wm.keyconfigs.addon.keymaps[km_name].keymap_items[:]:
                if kmi.idname == game_keys[key][1] and kmi.type == game_keys[key][2]:# and kmi.value == game_keys[type][3]:
                    print('..skip existing:', game_keys[key])
                    kmi_found = True
                    break
        if not kmi_found:
            if game_keys[key][0] == '3D View':
                km = wm.keyconfigs.addon.keymaps.new(name=game_keys[key][0], space_type='VIEW_3D') # '3D View',
            else:
                km = wm.keyconfigs.addon.keymaps.new(name=game_keys[key][0]) # 'Object Mode'
            print('..add KeyMap_Item:', game_keys[key])
            kmi = km.keymap_items.new(game_keys[key][1], game_keys[key][2], game_keys[key][3], ctrl=False, shift=False)#"view3d.walk", 'W', 'PRESS')
            addon_keymaps.append((km, kmi))


def unregister():
    # Remove the shortcut
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def init():
    print(f' => [{__name__}] init()')
    try:
        unregister()
    except:
        pass
    register()

if __name__ == "__main__":
    init()
#    unregister()
    
    
            