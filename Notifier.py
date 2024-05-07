import pygame
from winotify import Notification

class Notifier:
    def __init__(self):
        pygame.mixer.init()

        # Intialize different notifications for work, long break, 
        # short break, and end.
        self.work_toast = Notification(
            app_id="Pomodoro", 
            duration = "short", 
            title="Time to work!"
        )
        self.long_break_toast =Notification(
            app_id="Pomodoro", 
            duration = "short", 
            title="Time for a long break!"
        )
        self.short_break_toast =Notification(
            app_id="Pomodoro", 
            duration = "short", 
            title="Time for a short break!"
        )
        self.end_toast =Notification(
            app_id="Pomodoro", 
            duration = "short", 
            title="You have completed all your pomodoros! Congrats!"
        )
        
    def notify(self, session):
    # Notification sounds from https://noproblo.dayjo.org/ZeldaSounds/
        
        if session == "long break":
            self.long_break_toast.show()
            pygame.mixer.music.load("notifier_sounds/BOTW_Fanfare_SmallItem.wav")
        elif session == "short break":
            self.short_break_toast.show()
            pygame.mixer.music.load("notifier_sounds/BOTW_Fanfare_SmallItem.wav")
        elif session == "work":
            self.work_toast.show()
            pygame.mixer.music.load("notifier_sounds/BOTW_Secret.wav")
        elif session == "end":
            self.end_toast.show()
            pygame.mixer.music.load("notifier_sounds/BOTW_Fanfare_SpiritOrb.wav")

        pygame.mixer.music.play()

    def stop_sound(self):
        pygame.mixer.music.stop()