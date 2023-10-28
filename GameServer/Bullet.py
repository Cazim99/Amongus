import threading
import math
import uuid
import time
import pygame

class Bullet(threading.Thread):


    def __init__(self, root, x, y, owner, angle, max_travel=1000, bulletspeed=20):
        super().__init__(target='run', daemon=True)
        self.root = root
        self.x = x
        self.y = y
        self.owner = owner
        self.angle = angle
        self.travel_count = 0
        self.max_travel = max_travel
        self.bulletspeed = bulletspeed
        self.running = False
        self.uuid = str(uuid.uuid1())

        self.FPS = 120
        self.FramePerSec = pygame.time.Clock()
        self.current_fps = self.FPS

    def run(self):
        self.running = True
        while self.running:
            self.x = (self.x + round((self.bulletspeed * -math.sin(math.radians(self.angle)))))
            self.y = (self.y + round((self.bulletspeed * -math.cos(math.radians(self.angle)))))
            self.root.bullets[self.uuid] = [self.x, self.y]
            for user_username in self.root.users.keys():
                cordinates = self.root.users[user_username]['cordinates']
                rect = pygame.Rect(cordinates[0], cordinates[1], 50, 50)
                bullet_rect = pygame.Rect(self.x, self.y, 20, 20)

                if rect.colliderect(bullet_rect) \
                    and user_username != self.owner \
                        and self.root.users[user_username]['inside_ship']:
                    self.root.users[user_username]['health'] -= 3
                    self.running = False

            if self.travel_count >= self.max_travel:
                self.running = False
            else:
                self.travel_count += self.bulletspeed
            
            self.FramePerSec.tick(self.FPS)
            self.current_fps = self.FramePerSec.get_fps()
        self.root.bullets.pop(self.uuid)