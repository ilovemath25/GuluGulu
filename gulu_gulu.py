import pygame
from game import Player
from level.level1 import Level1
from level.level2 import Level2
from level.win import Win
pygame.init()
CLOCK = pygame.time.Clock()
GRAVITY = 1 ; WIDTH, HEIGHT = 1000, 600 ; FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gulu_gulu')
run = True
offset_x = [0]
current_size = "medium"
restart = False
# position
in_level_1 = True
in_level_2 = True
in_win = True
# class
player = Player(0, 0, "medium", "room1")
level1 = Level1()
level2 = Level2()
won = Win()
# main loop
while run:
   POS = pygame.mouse.get_pos()
   CLOCK.tick(FPS)
   if in_level_1:
      if player.current_room=="room1":
         if level1.room1.count==0: player = Player(100, -203, "medium", "room1")
         if not level1.room1.play: level1.room1.entry(WIN, player)
         else:
            level1.room1.draw(WIN, player)
            level1.room1.game_func(FPS, player)
         level1.room1.count+=1
         
      elif player.current_room=="room2":
         if level1.room2.count==0: player = Player(50, 440, "small", "room2")
         elif not level1.room2.play and level1.room2.count>100:
            if "key" in player.inventory:
               player = Player(1720, 150, "small", "room2")
               player.inventory.append('key')
            else: player = Player(1720, 150, "small", "room2")
            player.y_vel = -GRAVITY * 5
            level1.room2.play = True
         elif not level1.room2.play: level1.room2.entry(WIN, player)
         else:
            level1.room2.draw(WIN, player, offset_x)
            level1.room2.game_func(FPS, player, offset_x)
         level1.room2.count+=1
         in_level_1 = level1.room2.in_level1
         
      elif player.current_room=="room3":
         level1.room2.play = False
         if level1.room3.count<=1:
            if 'key' in player.inventory:
               player = Player(300, 0, "small", "room3")
               player.inventory.append('key')
            else: player = Player(300, 0, "small", "room3")
            player.y_vel = GRAVITY * 6
         if not level1.room3.play: level1.room3.entry(WIN, player)
         else:
            level1.room3.draw(WIN, FPS, player)
            level1.room3.game_func(FPS, player)
         player.keys(FPS, level1.room3.objects)
         level1.room3.count+=1
      
   elif in_level_2:
      if player.current_room=='room1':
         if level2.room1.count == 0:
            y_positions = {"small": 450, "medium": 350, "large": 150}
            player = Player(50, y_positions.get(current_size, 150), current_size, "room1")
         elif not level2.room1.play and level2.room1.count>100:
            player = Player(WIDTH//2+200, 0, current_size, "room1")
            player.y_vel = GRAVITY * 6
            level2.room1.play = True
            offset_x[0] = 300
         elif(not level2.room1.play): level2.room1.entry(WIN, player)
         else:
            level2.room1.draw(WIN, player, offset_x)
            level2.room1.game_func(FPS, player, offset_x)
         level2.room1.count+=1
         in_level_2 = level2.room1.in_level2
         level2.room1.temp = not level2.room2.temp

      elif player.current_room=='room2':
         if level2.room2.count<=1:
            player = Player(40, HEIGHT - 300, current_size, "room2")
            player.y_vel = -GRAVITY * 5
         if(not level2.room2.play): level2.room2.entry(WIN, player)
         else:
            level2.room2.draw(WIN, player)
            level2.room2.game_func(FPS, player)
         player.keys(FPS, level2.room2.objects)
         level2.room2.count+=1
         
   elif in_win:
      if(won.count==0): player = Player(WIDTH//2 - 75, HEIGHT//2 - 100, "medium", "room1")
      won.draw(WIN, FPS, player)
      restart = won.key()
      won.count+=1
   if restart:
      in_level_1 = True
      in_level_2 = True
      in_win = True
      level1 = Level1()
      level2 = Level2()
      won = Win()
      offset_x = [0]
      current_size = "medium"
      restart = False
   for event in pygame.event.get():
      if event.type == pygame.QUIT:run = False
      if event.type == pygame.KEYDOWN:
         if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE) and player.jump_count==0: player.jump()
         if(player.choose_size>0):
            if(event.key == pygame.K_1):player.shrink()
            elif(event.key == pygame.K_2):player.grow()
   current_size = player.size
   pygame.display.update()
pygame.quit()