import pygame
from winotify import Notification

class Notifier:
    def __init__(self):
        self.alarm = pygame.mixer.init()

        #Initializing windows notification 
        # Icon by Leremy https://www.freepik.com/icon/healthy_10049659#fromView=search&term=stretching&page=1&position=4&track=ais
        self.toast = Notification(app_id="Stretch Timer", title="Get up and stretch!",
                     duration = "short", icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\notificaiton_icon.png")

    def play_alarm(self):
        # Notification sound by Joao_Janz on freesound.org
        # https://freesound.org/people/Joao_Janz/sounds/504821/
        self.alarm.music.load("notification_sound.wav")
        self.alarm.music.play(loops=3)