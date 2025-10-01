import sys

import pygame
import scene_handler
from elements.py_button import Button
from elements.text import TextEdit, Text
from pygame_scene import PyGameScene
import requests

import online_handler
import value_handler
from level_renderer import TileWorld

BASE_URL = "http://45.93.249.98:8080"
def login(mail, password):
    email = mail
    passwd = password
    if isinstance(mail, TextEdit) and isinstance(passwd, TextEdit):
        email = mail.text
        passwd = passwd.text
    url = f"{BASE_URL}/api/auth/login"
    payload = {
        "email": email,
        "password": passwd
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Fehler werfen, falls HTTP != 200

        data = response.json()
        if "token" in data:
            value_handler.auth_token = data["token"]
            print(f"✅ Login erfolgreich! Token gespeichert: {value_handler.auth_token}")
            scene_handler.current_scene = MainMenu()
            return True
        else:
            print("❌ Login fehlgeschlagen: Kein Token in Antwort")

    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP-Fehler: {e}")
    return False
class LoadingScreen(PyGameScene):
    def __init__(self, mail, password):
        super().__init__()
        print("Loading Screen")
        if not login(mail, password):
            print("Couldn't login")
            scene_handler.current_scene = Login()
    def update(self):
        super().update()
        self.drawables.append(Text("LOADING...","arial",pygame.Rect(scene_handler.camera_size.x // 2, scene_handler.camera_size.y, 0,64)))

    def render(self, screen, events) -> bool:
        pygame.draw.rect(screen,(40,120,40),(0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        return super().render(screen, events)

class Login(PyGameScene):
    mail : str = ""
    passwd : str = ""
    def update(self):
        super().update()
        emailRect = pygame.Rect(0,0,250,40)
        emailRect.center = (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 - 90)
        passwdRect = pygame.Rect(0,0,250,40)
        passwdRect.center = (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 - 30)

        if len(sys.argv) >= 3:
            self.mail = sys.argv[2]
            self.passwd = sys.argv[3]
            scene_handler.current_scene = LoadingScreen(self.mail, self.passwd)
            return
        def register():
            scene_handler.current_scene = RegisterMenu()
        emailEdit = TextEdit(self.mail,"E-Mail","Boxy-Bold",emailRect)
        passwdEdit = TextEdit(self.passwd,"Password","Boxy-Bold",passwdRect,is_password=True)
        self.drawables.append(emailEdit)
        self.drawables.append(passwdEdit)
        self.drawables.append(Button("Login",(scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 + 30),(250,40),pygame.font.SysFont("Boxy-Bold",16),login,on_click_values=(emailEdit,passwdEdit)))
        self.drawables.append(
            Button("Register", (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 + 90), (250, 40),
                   pygame.font.SysFont("Boxy-Bold", 16), register))

    def render(self,surface,events):
        print("Rendering Loading Screen")
        pygame.draw.rect(surface,(40,120,40),(0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        return super().render(surface,events)

class RegisterMenu(PyGameScene):
    mail = ""
    passwd = ""
    username = ""
    BASE_URL = "http://45.93.249.98:8080"
    def update(self):
        super().update()
        nameRect = pygame.Rect(0,0,250,40)
        nameRect.center = (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 - 150)
        emailRect = pygame.Rect(0,0,250,40)
        emailRect.center = (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 - 90)
        passwdRect = pygame.Rect(0,0,250,40)
        passwdRect.center = (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 - 30)
        def register(mail, password, nameedit):
            email = mail
            passwd = password
            if isinstance(mail, TextEdit) and isinstance(passwd, TextEdit):
                email = mail.text
                passwd = passwd.text
            url = f"{self.BASE_URL}/api/auth/register"
            payload = {
                "email": email,
                "password": passwd,
                "playername": nameedit.text,
                "skin":0
            }

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()  # Fehler werfen, falls HTTP != 200

                data = response.json()
                print(data)
                if "status" in data:
                    if data["status"] == "registered":
                        login(mail,password)
                        return True
                else:
                    print("❌ Login fehlgeschlagen: Kein Token in Antwort")

            except requests.exceptions.RequestException as e:
                print(f"❌ HTTP-Fehler: {e}")
            return False
        def login_pressed():
            scene_handler.current_scene = Login()
        emailEdit = TextEdit(self.mail,"E-Mail","Boxy-Bold",emailRect)
        passwdEdit = TextEdit(self.mail,"Password","Boxy-Bold",passwdRect,is_password=True)
        nameEdit = TextEdit(self.username,"Username","Boxy-Bold",nameRect)
        self.drawables.append(emailEdit)
        self.drawables.append(passwdEdit)
        self.drawables.append(nameEdit)
        self.drawables.append(Button("Register",(scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 + 30),(250,40),pygame.font.SysFont("Boxy-Bold",16),register,on_click_values=(emailEdit,passwdEdit,nameEdit)))
        self.drawables.append(
            Button("Login", (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2 + 90), (250, 40),
                   pygame.font.SysFont("Boxy-Bold", 16), login_pressed))

    def render(self,surface,events):
        pygame.draw.rect(surface,(40,120,40),(0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        return super().render(surface,events)

class MainMenu(PyGameScene):
    def update(self):
        super().update()
        def multiplayer():
            scene_handler.current_scene = TileWorld()
        self.drawables.append(
            Button("Multiplayer", (scene_handler.camera_size.x // 2, scene_handler.camera_size.y // 2), (250, 40),pygame.font.SysFont("Boxy-Bold", 16),multiplayer),
        )
    def render(self,surface,events):
        pygame.draw.rect(surface,(40,120,40),(0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        return super().render(surface,events)