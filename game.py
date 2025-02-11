import pygame
from os.path import join
GRAVITY = 1 ; WIDTH, HEIGHT = 1000, 600
VERTICAL_BLOCK = ["floor", "sizeshift"]
HORIZONTAL_BLOCK = []
def is_passable(obj):
   if hasattr(obj, "is_passable") and obj.is_passable:return True
   return False
class Player(pygame.sprite.Sprite):
   SMALL = (75, 100)
   MEDIUM = (150, 200)
   BIG = (300, 400)
   
   # init
   def __init__(self, x, y, size, current_room):self.init(x, y, size, current_room)
   def init(self, x, y, size, current_room):
      super().__init__()
      self.size = size
      self.sizes = {
         "small": self.SMALL,
         "medium": self.MEDIUM,
         "big": self.BIG
      }
      self.img = self.load_image()
      self.option = [pygame.image.load(join("assets", "character", "size_option", f"{s}.png")).convert_alpha() for s in ["bigger", "smaller"]]
      self.rect = pygame.Rect(x, y, *self.sizes[size])
      self.x_vel = 0
      self.y_vel = 0
      self.fall_count = 0
      self.jump_count = 1
      self.animation_count = 0
      self.current_room = current_room
      self.direction = 'right'
      self.img_type = 'idle'
      self.apply_size(size)
      self.choose_size = 0
      self.inventory = []
   
   # load images
   def load_image(self):
      image = pygame.image.load(join("assets", "character", "character.png")).convert_alpha()
      return {
         "entry_fall": [image.subsurface(pygame.Rect(200 * i, 0, 200, 200)) for i in range(3)],
         "entry_get_up": [image.subsurface(pygame.Rect(200 * i, 200, 200, 200)) for i in range(6)],
         "idle": [image.subsurface(pygame.Rect(150 * i, 400, 150, 200)) for i in range(2)],
         "walk": [image.subsurface(pygame.Rect(150 * i, 600, 150, 200)) for i in range(12)],
         "jump": [image.subsurface(pygame.Rect(0, 800, 150, 200))],
         "fall": [image.subsurface(pygame.Rect(0, 1000, 150, 200))]
      }
   
   # size
   def shrink(self):
      temp = self.inventory
      if(self.size == "medium"):self.init(self.rect.x, self.rect.y-self.MEDIUM[1], "big", self.current_room)
      if(self.size == "small"):self.init(self.rect.x, self.rect.y-self.SMALL[1], "medium", self.current_room)
      self.inventory = temp
   def grow(self):
      temp = self.inventory
      if(self.size == "medium"):self.init(self.rect.x, self.rect.y, "small", self.current_room)
      if(self.size == "big"):self.init(self.rect.x, self.rect.y, "medium", self.current_room)
      self.inventory = temp
   def apply_size(self, size):
      new_size = self.sizes[size]
      self.rect.size = new_size
      for img in self.img:
         if('entry' not in img):self.img[img] = [pygame.transform.scale(img, new_size) for img in self.img[img]]
   
   # flip
   def flip(self):
      for img in self.img:
         if('entry' not in img):self.img[img] = [pygame.transform.flip(img, True, False) for img in self.img[img]]
   
   # movement
   def left(self):
      self.x_vel = -5
      if(self.direction != 'left'):
         self.direction = 'left'
         self.flip()
   def right(self):
      self.x_vel = 5
      if(self.direction != 'right'):
         self.direction = 'right'
         self.flip()
   def jump(self):
      self.y_vel = -GRAVITY * 11
      self.animation_count = 0
      self.jump_count = 1
   def fall(self,fps):
      self.y_vel+=min(1, (self.fall_count/fps) * GRAVITY)
      self.fall_count+=1
   
   # check image
   def check_img(self):
      if self.y_vel < 0:self.img_type = "jump"
      elif self.y_vel > GRAVITY*2:self.img_type = "fall"
      elif self.x_vel != 0:self.img_type = "walk"
      else:self.img_type = "idle"
      if self.img_type=='idle':self.animation_count+=0.05
      elif self.img_type=='walk':self.animation_count+=0.25
   
   # collide
   def vertical_collide(self, objects):
      collided_objects = []
      for obj in objects:
         if pygame.sprite.collide_rect(self, obj):
            if not is_passable(obj):
               if self.y_vel > 0:
                  self.rect.bottom = obj.rect.top
                  self.fall_count = 0
                  self.y_vel = 0
                  self.jump_count = 0
               elif self.y_vel < 0 and obj.rect.bottom<HEIGHT:
                  self.rect.top = obj.rect.bottom
                  self.y_vel*=-1
            collided_objects.append(obj)
      return collided_objects
   def horizontal_collide(self, objects, left_right):
      if left_right=='left':self.rect.x-=5
      elif left_right=='right':self.rect.x+=5
      self.rect.y-=2
      collided_object = None
      for obj in objects:
         if pygame.sprite.collide_rect(self, obj) and obj.name not in VERTICAL_BLOCK:
            collided_object = obj
            break
      if left_right=='left':self.rect.x+=5
      elif left_right=='right':self.rect.x-=5
      self.rect.y+=2
      return collided_object
   
   # draw option
   def draw_option(self, win, offset_x):
      offsetx = 120
      offsety_1 = 70
      offsety_2 = 30
      if self.size=="small":
         width, height = self.option[1].get_size()
         surface = pygame.Surface((width,height))
         surface.set_alpha(75)
         surface.blit(self.option[1],(0,0))
         win.blit(surface,(self.rect.x + offsetx - offset_x,self.rect.y + offsety_1))
      else:win.blit(self.option[1],(self.rect.x + offsetx - offset_x,self.rect.y + offsety_1))
      if self.size=="big":
         width, height = self.option[0].get_size()
         surface = pygame.Surface((width,height))
         surface.set_alpha(75)
         surface.blit(self.option[0],(0,0))
         win.blit(surface,(self.rect.x + offsetx - offset_x,self.rect.y + offsety_2))
      else:win.blit(self.option[0],(self.rect.x + offsetx - offset_x,self.rect.y + offsety_2))
      
   # draw
   def draw(self, win, offset_x=0):
      win.blit(self.img[self.img_type][int(self.animation_count) % len(self.img[self.img_type])],(self.rect.x - offset_x,self.rect.y))
      if(self.choose_size>0):self.draw_option(win, offset_x)

   # interaction with object
   def interact_obj(self, collide_check, key):
      for collide_obj in collide_check:
         if collide_obj:
            if collide_obj.name == "sizeshift":
               self.choose_size = 10
            elif collide_obj.name == "drawer":
               if self.size == "small" and self.rect.bottom - 20 < collide_obj.rect.top:self.current_room = "room3"
            elif collide_obj.name == "platform":
               if self.rect.bottom - 25 < collide_obj.rect.top:
                  collide_obj.is_passable = False
                  self.rect.bottom = collide_obj.rect.top
                  self.fall_count = 0
                  self.y_vel = 0
                  self.jump_count = 0
               else:collide_obj.is_passable = True
            elif hasattr(collide_obj, "is_movable") and collide_obj.is_movable:
               collide_obj.push(self, key)
            elif hasattr(collide_obj, "is_passable") and collide_obj.is_passable:
               if collide_obj.name=="key":
                  self.inventory.append("key")
                  collide_obj.is_taken = True
      
   # key
   def keys(self, fps, objects):
      self.fall(fps)
      self.rect.x+=self.x_vel
      self.rect.y+=self.y_vel
      self.x_vel = 0
      self.choose_size-=1
      key = pygame.key.get_pressed()
      collide_left = self.horizontal_collide(objects, 'left')
      collide_right = self.horizontal_collide(objects, 'right')
      if(key[pygame.K_LEFT] or key[pygame.K_a]) and (not collide_left or is_passable(collide_left)):self.left()
      elif(key[pygame.K_RIGHT] or key[pygame.K_d]) and (not collide_right or is_passable(collide_right)):self.right()
      vertical_collide = self.vertical_collide(objects)
      self.check_img()
      collide_check = [collide_left, collide_right, *vertical_collide]
      self.interact_obj(collide_check, key)

class Object(pygame.sprite.Sprite):
   def __init__(self, x, y, width, height, name, offsetx=0, offsety=0):
      super().__init__()
      self.rect = pygame.Rect(x, y, width, height)
      self.image = pygame.Surface((width, height), pygame.SRCALPHA)
      self.width = width
      self.height = height
      self.name = name
      self.offsetx = offsetx
      self.offsety = offsety
   
   def draw(self, win, offset_x=0):
      win.blit(self.image,(self.rect.x + self.offsetx - offset_x, self.rect.y + self.offsety))
      # pygame.draw.rect(win, (255, 0, 0),(self.rect.x - offset_x, self.rect.y, self.rect.width, self.rect.height), 2)
   
class GameObject(Object):
   def __init__(self, x, y, width, height, image_path, name, offsetx=0, offsety=0):
      super().__init__(x, y, width, height, name, offsetx, offsety)
      block = pygame.image.load(image_path).convert_alpha()
      block = pygame.transform.scale(block, (width, height))
      self.image.blit(block, (0, 0))

class MovableObject(GameObject):
   def __init__(self, x, y, width, height, image_path, name, offsetx=0, offsety=0, allowed_sizes=[]):
      super().__init__(x, y, width, height, image_path, name, offsetx, offsety)
      self.is_movable = True
      self.allowed_sizes = allowed_sizes
      self.count = 0
   
   def push(self, player, key):
      if player.size in self.allowed_sizes:
         if player.rect.bottom - 20 > self.rect.top:
            if player.rect.left <= self.rect.left:
               if (key[pygame.K_RIGHT] or key[pygame.K_d]):self.count = 10
               self.rect.x+=2
               if(self.count):player.img_type = "walk"
               else:player.img_type = "idle"
            elif player.rect.right >= self.rect.right:
               if (key[pygame.K_LEFT] or key[pygame.K_a]):self.count = 10
               self.rect.x-=2
               if(self.count):player.img_type = "walk"
               else:player.img_type = "idle"
            if(self.count>0):self.count-=1

class PassableObject(GameObject):
   def __init__(self, x, y, width, height, image_path, name, offsetx=0, offsety=0):
      super().__init__(x, y, width, height, image_path, name, offsetx, offsety)
      self.is_passable = True

class Block(GameObject):
   def __init__(self, x, y, width, height, image_path=join("assets", "block.png"), name=None):
      super().__init__(x, y, width, height, image_path, name)

class SizeShift(GameObject):
   def __init__(self, x, y, width, height, image_path=join("assets", "sizeshift.png")):
      super().__init__(x, y, width, height, image_path, "sizeshift", offsetx=-50, offsety=-30)
      self.rect = pygame.Rect(x, y, width - 100, height)

class Chair(MovableObject):
   def __init__(self, x, y, width, height, image_path, allowed_sizes):
      super().__init__(x, y, width, height, image_path, "chair", offsety=-140, allowed_sizes=allowed_sizes)
      self.rect = pygame.Rect(x, y, width, height - 140)

class BlockMove(MovableObject):
   def __init__(self, x, y, width, height, image_path, allowed_sizes):
      super().__init__(x, y, width, height, image_path, "blockmove", offsety=-20, allowed_sizes=allowed_sizes)

class Desk(Block):
   def __init__(self, x, y, width, height, image_path):
      super().__init__(x, y, width, height, image_path, "desk")

class Drawer(Block):
   def __init__(self, x, y, width, height, image_path):
      super().__init__(x, y, width, height, image_path, "drawer")

class Key(PassableObject):
   def __init__(self, x, y, width, height, image_path=join("assets", "level1", "room3", "key.png")):
      super().__init__(x, y, width, height, image_path, "key")
      self.is_taken = False

class Door(Block):
   def __init__(self, x, y, width, height, image_path):
      super().__init__(x, y, width, height, image_path, "door")

class Platform(PassableObject):
   def __init__(self, x, y, width, height, image_path=join("assets", "level2", "room1", "platform.png")):
      super().__init__(x, y, width, height, image_path, "platform")