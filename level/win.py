import pygame
from os.path import join
WIDTH, HEIGHT = 1000, 600 ; FPS = 60
sizeshift_size = [200, 60]
class Win:
   def __init__(self) -> None:
      self.bg = pygame.image.load(join("assets", "escape.png")).convert_alpha()
      self.restart = pygame.transform.scale(pygame.image.load(join("assets", "restart.png")).convert_alpha(),(252, 72))
      self.count = 0
   def draw(self, win, fps, player):
      win.blit(self.bg, (0, 0))
      player.draw(win)
      player.animation_count+=0.05
      if(self.count>100):win.blit(self.restart, (WIDTH//2 - 126, HEIGHT - 150))
   def key(self):
      key = pygame.key.get_pressed()
      if(key[pygame.K_1]):return True
      return False