import pygame
from winotify import Notification
class Notifier:
    def __init__(self):
        pygame.mixer.init()

        # Creating a different notification for work, long break, short break, and end
        self.work_toast = Notification(app_id="Pomodoro", duration = "short", title="Time to work!",
                                  icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\icons\notifier_icon.png")
        self.long_break_toast =Notification(app_id="Pomodoro", duration = "short", title="Time for a long break!",
                                  icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\icons\notifier_icon.png")
        self.short_break_toast =Notification(app_id="Pomodoro", duration = "short", title="Time for a short break!",
                                  icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\icons\notifier_icon.png")
        self.end_toast =Notification(app_id="Pomodoro", duration = "short", title="You have completed all your pomodoros! Congrats!",
                                  icon=r"C:\Users\Bailey\Documents\GitHub\Timer-App\icons\notifier_icon.png")
        
    # Notification sounds from https://noproblo.dayjo.org/ZeldaSounds/ 
    def play_sound(self, sound):
        if sound == "break":
            pygame.mixer.music.load("notifier_sounds/BOTW_Fanfare_SmallItem.wav")
        elif sound == "work":
            pygame.mixer.music.load("notifier_sounds/BOTW_Secret.wav")
        elif sound == "end":
            pygame.mixer.music.load("notifier_sounds/BOTW_Fanfare_SpiritOrb.wav")

        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()