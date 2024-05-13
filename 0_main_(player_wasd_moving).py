'''
Enrty point.
Info: https://blenderartists.org/t/bege-module-keyconfig-player-wasd-movement
'''
import bpy

__name__ = '[main.py]'
print(__name__)

module_player = bpy.data.texts["module_player.py"].as_module()

scene = bpy.context.scene
#player = module_player.init(scene.objects['Cube']) #scene.objects['Camera']) # remove parent and ? dooble run main.py 
player = module_player.init(scene.objects['Rocket Launcher'])
scene["player"] = player

module_keyconfig = bpy.data.texts["module_keyconfig.py"].as_module()
module_keyconfig.init() # <= need scene["player"]


def game_loop(self, context):
    module_player.update(player)
      
bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(game_loop) # ON-OFF game_loop



