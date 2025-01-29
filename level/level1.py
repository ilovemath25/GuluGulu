import pygame
from os.path import join
from game import *
SIZE = 30
SIZESHIFT_SIZE = [200, 60]
CHAIR_SIZE = [170, 270]
WIDTH, HEIGHT = 1000, 600
class Room1:
   def __init__(self, width, height) -> None:
      self.width = width
      self.height = height
      self.bg = [pygame.transform.scale(pygame.image.load(join("assets", "level1", "room1", f"bg_{i}.png")).convert_alpha(), (self.width, self.height)) for i in range(2)]
      self.obj_init()
      self.count = 0
      self.play = False
      
   def obj_init(self):
      self.floor = [Block(i*SIZE, self.height - SIZE, SIZE, SIZE) for i in range(0, self.width//SIZE)]
      self.wall1 = [Block(0, i*SIZE, SIZE, SIZE) for i in range(0, self.height//SIZE)]
      self.wall2 = [Block(self.width - SIZE, i*SIZE, SIZE, SIZE) for i in range(0, self.height//SIZE - 5)]
      self.sizeshift = SizeShift(self.width//2 + 35, self.height - SIZESHIFT_SIZE[1], SIZESHIFT_SIZE[0], SIZESHIFT_SIZE[1])
      self.objects = [*self.floor, *self.wall1, *self.wall2, self.sizeshift]
      
   def draw(self, win, player):
      win.blit(self.bg[(self.count//4) % len(self.bg)], (0,0))
      for obj in self.objects:obj.draw(win)
      player.draw(win)
      
   def entry(self, win, player):
      win.blit(self.bg[(self.count//4) % len(self.bg)], (0,0))
      for obj in self.objects:obj.draw(win)
      if(self.count==0):player.img_type = "entry_fall"
      elif(10<self.count<200):
         if(player.rect.y<372):player.rect.y+=23
         elif(player.animation_count<len(player.img[player.img_type])-1):player.animation_count+=0.3
         player.draw(win)
      elif(self.count==200):
         player.animation_count = 0
         player.img_type = "entry_get_up"
      elif(200<self.count<250):
         if(player.animation_count<len(player.img[player.img_type])-1):player.animation_count+=0.3
         player.draw(win)
      elif(250<=self.count):
         self.play = True
         player.rect.x-=7
         player.rect.y-=12
         player.img_type = "idle"
         player.draw(win)
         
   def game_func(self, fps, player):
      player.keys(fps, self.objects)
      if player.rect.x > self.width-30: player.current_room = "room2"

class Room2:
   def __init__(self, width, height) -> None:
      self.width = width
      self.height = height
      self.bg = [pygame.transform.scale(pygame.image.load(join("assets", "level1", "room2", f"bg_{i}.png")).convert_alpha(), (self.width, self.height)) for i in range(2)]
      self.obj_init()
      self.count = 0
      self.play = False
      self.locked = True
      self.in_level1 = True
      
   def obj_init(self):
      self.floor = [Block(i*SIZE, self.height - 2*SIZE, SIZE, SIZE) for i in range(0, self.width//SIZE)]
      self.wall1 = [Block(0, i*SIZE, SIZE, SIZE) for i in range(0, self.height//SIZE)]
      self.chair1 = Chair(31*SIZE, self.height//2 + 4*SIZE, CHAIR_SIZE[0], CHAIR_SIZE[1], join("assets", "level1", "room2", "chair.png"), ["big", "medium"])
      self.chair2 = Chair(self.width - 23*SIZE, self.height//2 + 4*SIZE, CHAIR_SIZE[0], CHAIR_SIZE[1], join("assets", "level1", "room2", "chair.png"), ["big", "medium"])
      self.sizeshift = SizeShift(17*SIZE, self.height - 1.3*SIZESHIFT_SIZE[1], SIZESHIFT_SIZE[0], SIZESHIFT_SIZE[1])
      self.desk = Desk(self.width//2 + 11*SIZE, self.height//2 - 50, 350, 290, join("assets", "level1", "room2", "desk.png"))
      self.drawer = Drawer(self.width//2 + 6*SIZE, self.height//2 - 20, 260, 120, join("assets", "level1", "room2", "drawer.png"))
      self.door = Door(self.width - 4.45*SIZE, 0, 133, 600, join("assets", "level1", "room2", "door.png"))
      self.door_locked = pygame.image.load(join("assets","door_locked.png")).convert_alpha()
      self.objects = [*self.floor, *self.wall1, self.sizeshift, self.chair1, self.desk, self.drawer, self.chair2, self.door]
      self.objects2 = [*self.floor, *self.wall1, self.sizeshift, self.chair1, self.desk, self.drawer, self.chair2]
      
   def draw(self, win, player, offset_x):
      win.blit(self.bg[(self.count//5) % len(self.bg)], (-offset_x[0], 0))
      for obj in self.objects:obj.draw(win, offset_x[0])
      if(player.rect.right>=2850):
         if "key" not in player.inventory:win.blit(self.door_locked, (WIDTH//2 - 150, 90))
      player.draw(win, offset_x[0])
      
   def entry(self, win, player):
      win.blit(self.bg[(self.count//5) % len(self.bg)], (0,0))
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
      if(self.chair1.rect.right > self.drawer.rect.left):
         self.chair1.rect.right = self.drawer.rect.left
      if(self.chair1.rect.left < self.sizeshift.rect.right):
         self.chair1.rect.left = self.sizeshift.rect.right
      if(self.chair2.rect.left < self.desk.rect.right):
         self.chair2.rect.left = self.desk.rect.right
      if(player.rect.right>=2850):
         if("key" in player.inventory):
            self.objects = self.objects2
            self.locked = False
      if(player.rect.x>2950):
         self.in_level1 = False
         player.current_room = "room1"
         offset_x[0] = 0
      if((player.rect.right - offset_x[0] >= WIDTH//2) and player.x_vel > 0 and offset_x[0] < self.width-WIDTH) or (
         (player.rect.left - offset_x[0] <= WIDTH//2) and player.x_vel < 0 and offset_x[0] >= 0):
         offset_x[0] += player.x_vel
   
class Room3:
   def __init__(self, width, height) -> None:self.init(width, height)
   def init(self, width, height):
      self.width = width
      self.height = height
      self.bg = pygame.transform.scale(pygame.image.load(join("assets", "level1", "room3", "bg.png")).convert_alpha(), (self.width, self.height))
      self.obj_init()
      self.count = 0
      self.play = False
   
   def obj_init(self):
      self.dark_bg = pygame.transform.scale(pygame.image.load(join("assets", "level1", "room3", "dark_bg.png")).convert_alpha(), (self.width, self.height))
      self.floor = [Block(i*SIZE, self.height-SIZE*7, SIZE, SIZE) for i in range(0, self.width//SIZE)]
      self.wall1 = [Block(SIZE*8, i*SIZE, SIZE, SIZE) for i in range(0, self.height//SIZE)]
      self.wall2 = [Block(self.width - SIZE*9, i*SIZE, SIZE, SIZE) for i in range(0, self.height//SIZE)]
      self.wall3 = [Block(self.width//2 - SIZE, i*SIZE, SIZE, SIZE) for i in range(6)]
      self.ceiling = [Block(self.width//2 + i*SIZE - SIZE, SIZE*6, SIZE, SIZE) for i in range(0, self.width//2//SIZE)]
      self.key = Key(self.width//2 + 2*SIZE, self.height//2 + 1.6*SIZE, 42, 14)
      self.objects = [*self.floor, *self.wall1, *self.wall2, *self.wall3, *self.ceiling, self.key]
      self.objects2 = [*self.floor, *self.wall1, *self.wall2, *self.wall3, *self.ceiling]
      
   def draw(self, win, fps, player):
      win.blit(self.bg, (0, 0))
      for obj in self.objects:obj.draw(win)
      player.draw(win)
      win.blit(self.dark_bg, (0,0))
      
   def entry(self, win, player):
      win.blit(self.bg, (0, 0))
      for obj in self.objects:obj.draw(win)
      player.draw(win)
      win.blit(self.dark_bg, (0,0))
      if(player.y_vel==0):self.play = True
      
   def game_func(self, fps, player):
      if(player.rect.y<150 and self.play):
         player.current_room = "room2"
         if self.key.is_taken:
            self.init(self.width, self.height)
            self.key.is_taken = True
         else:self.init(self.width, self.height)
      if(self.key.is_taken):self.objects = self.objects2
   
class Level1:
   def __init__(self) -> None:
      self.room1 = Room1(1000, 600)
      self.room2 = Room2(3000, 600)
      self.room3 = Room3(1000, 600)
      self.current = 'room1'