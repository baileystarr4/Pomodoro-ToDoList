import pygame
from winotify import Notification
class Notifier:
    def __init__(self):
        pygame.mixer.init()

        #Initializing windows notification 
        # Icon by Leremy https://www.freepik.com/icon/healthy_10049659#fromView=search&term=stretching&page=1&position=4&track=ais
        self.work_toast = Notification(app_id="Stretch Timer", duration = "short", title="Time to work!",
                                  icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\notificaiton_icon.png")
        self.break_toast =Notification(app_id="Stretch Timer", duration = "short", title="Time to break!",
                                  icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\notificaiton_icon.png")

    def play_alarm(self):
        # Notification sound by Joao_Janz on freesound.org
        # https://freesound.org/people/Joao_Janz/sounds/504821/
        pygame.mixer.music.load("notification_sound.wav")
        pygame.mixer.music.play(loops=3)
    
    def stop_music(self):
        pygame.mixer.music.stop()