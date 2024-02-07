# https://devsecopsguides.com/docs/rules/python/#unprotected-storage-of-credentials

# Authorisation Module
# User authorisation & save login:password to local file
# Code by: @o.shcherbyna
# ver: 0.2


import bpy
import hashlib
import os
from bpy_extras import view3d_utils


file_name = "credentials.txt"
file_path = os.path.join(os.path.dirname(bpy.data.filepath), file_name)

bpy.context.scene['msg'] = [] # to share data between dialog boxes in this module
bpy.context.scene['user'] = "" # to use in game. Exp: USER = bpy.data.scenes['Login']['user'] 

LOGIN_EXIST = 2
    
def save_credentials(username, password, check_login=False):
    '''Saves data if login does not exist'''
    if check_login:
        is_login_exist = check_credentials(username, password, check_only_login = True)
        if is_login_exist == LOGIN_EXIST:
            return False

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    credentials = f"{username}: {hashed_password}\n"
    
    with open(file_path, "a") as credentials_file:
        credentials_file.write(credentials)
#    print('True  # Нового користувача додано')
    return True  # new data saved

def check_credentials(input_username, input_password, check_only_login = False):
    '''Checks stored login/password.
        Can check only login.
    '''
    # Хешуємо введений пароль
#    hashed_input_login = hashlib.sha256(input_username.encode()).hexdigest()
    hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
    
    # Відкриваємо файл credentials.txt для читання
    with open(file_path, "r") as credentials_file:
        # Зчитуємо всі рядки з файлу
        lines = credentials_file.readlines()
        
        # Проходимо через кожен рядок
        for line in lines:
            # Розділяємо рядок на частини (логін та хеш паролю)
            parts = line.split(": ")
#            stored_hashed_login = parts[0].strip()
            stored_login = parts[0].strip()
            
            if check_only_login:
                if input_username == stored_login:
                    return LOGIN_EXIST
                else: continue
                
            stored_hashed_password = parts[1].strip()
            
            # Перевіряємо, чи логін та хеш паролю співпадають
#            if hashed_input_login == stored_hashed_login and hashed_input_password == stored_hashed_password:
            if input_username == stored_login and hashed_input_password == stored_hashed_password:
                print('True  # Успішна аутентифікація')
                return True  # success
    
    # Якщо не знайдено відповідний запис
    print('False  # Невірний логін або пароль')
    return False  # login/pass doesn't correct

class OP_ADD_NEW_USER(bpy.types.Operator):
    bl_idname = "game.add_new_user"
    bl_label = "Add New User"
    bl_description = "Create a new player Account"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        result = False
        result = save_credentials(context.scene['msg'][0], context.scene['msg'][1], check_login=True)#self.login, self.pswd)
        if result:
            context.scene['user'] = context.scene['msg'][0]#self.login
#            set_mouse_to(bpy.context.scene.cursor, 160, -70)
#            print(f'[{__name__}] > game.add_new_user > execute({result})')
#            context.scene['msg'] = ['Success', ': New account has been created']
#            context.window_manager.popup_menu(popup_msgbox, title='Info', icon='INFO')
            bpy.context.scene.camera.location.y = -10.0
            return {'FINISHED'}
        else:
            bpy.ops.game.back_to_login('EXEC_DEFAULT')
            set_mouse_to(bpy.context.scene.cursor, 140, 50)
#            print(f'[{__name__}] > game.add_new_user > execute({result})')
            context.scene['msg'] = ['Error', ': Account is taken. Try another.']#['Error', ': New account has not been created']
            context.window_manager.popup_menu(popup_msgbox, title='Info', icon='INFO')
            return {'CANCELLED'}
    
class OP_BACK_TO_LOGIN(bpy.types.Operator):
    bl_idname = "game.back_to_login"
    bl_label = "Back to Login"
    bl_description = "Back to Login"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        set_mouse_to(bpy.context.scene.cursor)
        bpy.ops.game.loginbox('INVOKE_DEFAULT')
        return {'FINISHED'}

def popup_login_fail(self, context):
    layout = self.layout
    row = layout.row()
    row.label(text = 'Login or Password is wrong.', icon = "SEQUENCE_COLOR_01")#'QUESTION')#ERROR
    row = layout.box()
    props = row.operator("game.add_new_user", text="New Player", icon='COMMUNITY')#, desc='Create a new Player')
    row = layout.row()
    props = row.operator("game.back_to_login", text="Back", icon='BACK')

def popup_fild_empty(self, context):
    layout = self.layout
    row = layout.row()
    row.label(text = 'Login or Password is empty.', icon = "SEQUENCE_COLOR_01")#'QUESTION')#ERROR

def popup_msgbox(self, context):
    icons = {
    'Error': 'SEQUENCE_COLOR_01',
    'Question': 'SEQUENCE_COLOR_03',
    'Success': 'SEQUENCE_COLOR_04',
    }
    layout = self.layout
    row = layout.row()
    msg = context.scene['msg'][0] + context.scene['msg'][1]
    row.label(text = msg, icon = icons[context.scene['msg'][0]])#"SEQUENCE_COLOR_04")#'QUESTION')#ERROR
    context.scene['msg'] = []
 
 
class LoginBox(bpy.types.Operator):
    bl_idname = "game.loginbox"
    bl_label = "Log In / New Account"
    bl_options = {'REGISTER', 'UNDO'}

    login : bpy.props.StringProperty(name="Login", maxlen=20, description='Enter user login')
    pswd : bpy.props.StringProperty(name="Password", subtype='PASSWORD', maxlen=20, description='Enter user password')
  
#    def cancel(self, context):
#        bpy.ops.game.loginbox('INVOKE_DEFAULT') # keep window for authentification
    
    def execute(self, context):
        if not self.login or not self.pswd:
            set_mouse_to(bpy.context.scene.cursor)
            bpy.ops.game.loginbox('INVOKE_DEFAULT') # return to authentification dialog
            context.window_manager.popup_menu(popup_fild_empty, title='Error', icon='ERROR')
            return {'CANCELLED'}
  
        result = False
        try:
            result = check_credentials(self.login, self.pswd)
        except FileNotFoundError:
            save_credentials(self.login, self.pswd)
            context.scene['user'] = self.login
#            set_mouse_to(bpy.context.scene.cursor, 160, -70)
#            context.scene['msg'] = ['Success', ': New account has been created']
#            context.window_manager.popup_menu(popup_msgbox, title='Info', icon='INFO')
            bpy.context.scene.camera.location.y = -10.0
            return {'FINISHED'}
            
        if result:
            print(f'[{__name__}] > execute() > result: {result}')
            context.scene['user'] = self.login
#            set_mouse_to(bpy.context.scene.cursor, 110, -70)
#            context.scene['msg'] = ['Success', ' authentification']
#            context.window_manager.popup_menu(popup_msgbox, title='Info', icon='INFO')
            bpy.context.scene.camera.location.y = -10.0
            return {'FINISHED'}
        else:
            set_mouse_to(bpy.context.scene.cursor, 170, -130)
            context.scene['msg'] = [self.login, self.pswd] # store data for add_new_user operator
            context.window_manager.popup_menu(popup_login_fail, title='Info', icon='INFO')
            return {'CANCELLED'} # wrong login/pass => add_new/back popup
 
    def invoke(self, context, event):
        context.scene['msg'] = [] # reset
        context.scene['user'] = ""
        return context.window_manager.invoke_props_dialog(self, width=250)

 
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "login")
        row = layout.row()
        row.prop(self, "pswd")

def set_mouse_to(obj, offset_x=0, offset_y=0):
    '''
    Sets mouse cursor to object's (obj) location in VIEW_3D area.
    '''
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            # Отримати регіон та налаштування 3D вигляду
            region = area.regions[-1]
            rv3d = area.spaces.active.region_3d
            co_3d = obj.location

            # Конвертувати 3D координати в піксельні 2D координати
            co_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, co_3d)
#            print(co_2d)
            if co_2d:
                # Додати 2D координати до координат регіону 'VIEW_3D'
                x, y = co_2d.x + region.x, co_2d.y + region.y
    #            print(x, y)
                bpy.context.window.cursor_warp(int(x+offset_x), int(y+offset_y))
                return True
            else:
                print("co_2d =", co_2d)
                print(f'ERROR: [{__name__}] set_mouse_to(obj) > the OBJ should be in front of the CAMERA.')
                return False
    
    if 'region' not in locals():
        print(f'ERROR: [{__name__}] set_mouse_to(obj) > VIEW_3D area not found.')
        return False

def register():
    bpy.utils.register_class(OP_ADD_NEW_USER)
    bpy.utils.register_class(OP_BACK_TO_LOGIN)
    bpy.utils.register_class(LoginBox)
 
def unregister():
    bpy.utils.unregister_class(OP_ADD_NEW_USER)
    bpy.utils.unregister_class(OP_BACK_TO_LOGIN)
    bpy.utils.unregister_class(LoginBox)
    
def init():
    print(f' => [{__name__}] init()')
    try: unregister()
    except RuntimeError: pass
    register()
    bpy.context.scene.camera.location.y = -5.0
    # Set mouse to 3d_cursor.location (center of VIEW_3D)
    set_mouse_to(bpy.context.scene.cursor)
    # Show login box
    bpy.ops.game.loginbox('INVOKE_DEFAULT')

if __name__ == "__main__":
    register()
#    bpy.data.texts["module_auth.py"].use_module = True # Run auto 
    bpy.context.scene.camera.location.y = -5.0
    set_mouse_to(bpy.context.scene.cursor)
    auth = bpy.ops.game.loginbox('INVOKE_DEFAULT')
#    print("auth", auth)
