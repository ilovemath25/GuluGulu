import pygame
from os.path import join
from game import *
WIDTH, HEIGHT = 1000, 600 ; FPS = 60
SIZE = 30
SIZESHIFT_SIZE = [200, 60]
class Room1:
   def __init__(self, width, height) -> None:
      self.width = width
      self.height = height
      self.bg = [pygame.transform.scale(pygame.image.load(join("assets", "level2", "room1", f"bg_{i}.png")).convert_alpha(), (self.width, self.height)) for i in range(2)]
      self.land = pygame.transform.scale(pygame.image.load(join("assets", "level2", "room1", "land.png")).convert_alpha(), (self.width, self.height))
      self.opened_door = pygame.transform.scale(pygame.image.load(join("assets", "level2", "room1", "opened_door.png")).convert_alpha(), (self.width, self.height))
      self.obj_init()
      self.count = 0
      self.play = False
      self.locked = True
      self.temp = False
      self.in_level2 = True
      
   def obj_init(self):
      self.floor = [Block(i*SIZE, self.height - 2*SIZE + 10, SIZE, SIZE) for i in range(0, self.width//SIZE)]
      self.ceiling = [Block(i*SIZE + 9*SIZE, -SIZE*3, SIZE, SIZE) for i in range(0, 200//SIZE)]
      self.wall1 = [Block(0, i*SIZE, SIZE, SIZE) for i in range(0, self.height//SIZE)]
      self.block1 = BlockMove(self.width//2 + 10*SIZE, self.height - 7.5*SIZE, 220, 220, join("assets", "level2", "block1.png"), ["big"])
      self.block2 = BlockMove(self.width//2 + 11.5*SIZE, self.height - 6.5*SIZE, 180, 180, join("assets", "level2", "block2.png"), ["big", "medium"])
      self.platform = [Platform(SIZE*3, self.height - 6*SIZE*(i+1)-SIZE, 210, 60) for i in range(2)]
      self.sizeshift = SizeShift(18*SIZE, self.height - 2.3*SIZE, SIZESHIFT_SIZE[0], SIZESHIFT_SIZE[1])
      self.door = Door(1899, 0, 101, 600, join("assets", "level2", "room1", "door.png"))
      self.door_locked = pygame.image.load(join("assets","door_locked.png")).convert_alpha()
      self.objects = [*self.floor, *self.wall1, self.sizeshift, self.block1, self.door, *self.ceiling]
      self.objects1 = [*self.floor, *self.wall1, self.sizeshift, self.block1, self.door, *self.ceiling]
      self.objects2 = [*self.floor, *self.wall1, self.sizeshift, self.block1, *self.platform, self.door, *self.ceiling]
      self.objects3 = [*self.floor, *self.wall1, self.sizeshift, self.block1, self.block2, *self.platform, self.door, *self.ceiling]
      self.objects4 = [*self.floor, *self.wall1, self.sizeshift, self.block1, self.block2, *self.platform, *self.ceiling]
   
   def draw(self, win, player, offset_x):
      win.blit(self.bg[(self.count//5) % len(self.bg)], (-offset_x[0], 0))
      win.blit(self.opened_door, (-offset_x[0], 0))
      win.blit(self.land, (-offset_x[0], 15))
      for obj in self.objects:obj.draw(win, offset_x[0])
      if(player.rect.right>=1885):
         if self.locked:win.blit(self.door_locked, (WIDTH//2 - 150, 90))
      player.draw(win, offset_x[0])

   def entry(self, win, player):
      win.blit(self.bg[(self.count//5) % len(self.bg)], (0,0))
      win.blit(self.land, (0, 15))
      for obj in self.objects:obj.draw(win)
      if(self.count<=1):player.img_type = "walk"
      elif(1<self.count<60):
         if(player.rect.x<200):
            player.rect.x+=3
            player.animation_count+=0.2
         player.draw(win)
      elif(self.count==60):
         player.animation_count = 0
         player.img_type = "idle"
      elif(60<self.count):
         self.play = True
         player.img_type = "idle"
         player.draw(win)
         
   def game_func(self, fps, player, offset_x):
      player.keys(fps, self.objects)
      if(self.block1.rect.right > self.door.rect.left):
         self.block1.rect.right = self.door.rect.left
      if(self.block1.rect.left < self.sizeshift.rect.right):
         self.block1.rect.left = self.sizeshift.rect.right
      if(self.block2.rect.right > self.door.rect.left):
         self.block2.rect.right = self.door.rect.left
      if player.direction=="right" and self.block1.rect.right > self.block2.rect.left:
         self.block1.rect.right = self.block2.rect.left
      if player.direction=="left" and self.block2.rect.left < self.block1.rect.right:
         self.block2.rect.left = self.block1.rect.right
      if player.rect.y < -100 and player.rect.x < 400:
         player.current_room = "room2"
         self.play = False
      if self.block1.rect.x in range(750, 790):
         self.objects = self.objects2
      else:self.objects = self.objects1
      if self.temp:
         self.objects = self.objects3
      if self.block2.rect.x in range(1035, 1075):
         self.objects = self.objects4
         self.locked = False
      if player.rect.x > 1950:
         self.in_level2 = False
      if((player.rect.right - offset_x[0] >= WIDTH//2) and player.x_vel > 0 and offset_x[0] < self.width - WIDTH) or (
         (player.rect.left - offset_x[0] <= WIDTH//2) and player.x_vel < 0 and offset_x[0] >= 0):
         offset_x[0] += player.x_vel

class Room2:
   def __init__(self, width, height) -> None:self.init(width, height, True)
   def init(self, width, height, temp):
      self.width = width
      self.height = height
      self.temp = temp
      self.bg = pygame.transform.scale(pygame.image.load(join("assets", "level2", "room2","bg.png")).convert_alpha(),(2000,600))
      self.obj_init()
      self.count = 0
      self.play = False
   
   def obj_init(self):
      self.floor = [Block(i*SIZE, HEIGHT-SIZE*3, SIZE, SIZE, join("assets", "block.png")) for i in range(0,WIDTH//SIZE//2+5)]
      self.wall1 = [Block(0, i*SIZE, SIZE, SIZE, join("assets", "block.png")) for i in range(0,HEIGHT//SIZE)]
      if(self.temp):
         self.block2 = BlockMove(WIDTH//2-100, HEIGHT-SIZE*8, 180, 180, join("assets", "level2", "block2.png"), ["big", "medium"])
         self.objects = [*self.wall1, self.block2]
      else:self.objects = [*self.wall1]
      
   def draw(self, win, player):
      win.blit(self.bg, (0, 0))
      for obj in self.objects:obj.draw(win)
      player.draw(win)
      
   def entry(self, win, player):
      win.blit(self.bg, (0, 0))
      player.draw(win)
      if player.rect.y < self.height - 300:
         if self.temp:self.objects = [*self.floor, *self.wall1, self.block2]
         else:self.objects = [*self.floor, *self.wall1]
         self.play = True
      for obj in self.objects:obj.draw(win)
      
   def game_func(self, fps, player):
      if self.block2.rect.x > 650:
         self.block2.rect.y+=10
         self.temp = False
      if player.rect.y > HEIGHT:
         player.current_room = "room1"
         self.init(self.width, self.height, self.temp)
         self.play = False
      
class Level2:
   def __init__(self) -> None:
      self.room1 = Room1(2000, 600)
      self.room2 = Room2(1000, 600)
      self.current = 'room1'