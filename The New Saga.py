import pygame,sys,random
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
#Game variables
Screen_width=900
Screen_height=600
Screen=pygame.display.set_mode((Screen_width,Screen_height))
Hi_score=0
game_over=False
exit_game=False
Bgimg=pygame.image.load('space.png')
Bgimg=pygame.transform.scale(Bgimg,(Screen_width,Screen_height)).convert_alpha()
fps=60
VEL=2
enemy_Vel=4 
#Load images
RED_SPACE_SHIP = pygame.image.load("spaceship_red.png")
RED_SPACE_SHIP=pygame.transform.scale(RED_SPACE_SHIP,(45,50)).convert_alpha()
DARK_SPACE_SHIP = pygame.image.load("enemy ship.png")
DARK_SPACE_SHIP= pygame.transform.rotate(pygame.transform.scale(DARK_SPACE_SHIP,(45,50)).convert_alpha(),180)
DARK_SPACE_SHIP_2 = pygame.image.load( "enemy ship(2).png")
DARK_SPACE_SHIP_2=pygame.transform.rotate(pygame.transform.scale(DARK_SPACE_SHIP_2,(45,50)).convert_alpha(),180)
# # Player player
YELLOW_SPACE_SHIP = pygame.image.load("spaceship_yellow.png")
YELLOW_SPACE_SHIP= pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_SHIP,(45,50)).convert_alpha(),180)
# # Lasers
RED_LASER = pygame.image.load("Fireball.png")
RED_LASER=pygame.transform.rotate(pygame.transform.scale(RED_LASER,(10,15)).convert_alpha(),-90)

BLUE_LASER = pygame.image.load("Fireball_1.png")
BLUE_LASER=pygame.transform.rotate(pygame.transform.scale(BLUE_LASER,(10,15)).convert_alpha(),90)

PURPLE_LASER = pygame.image.load("energyball.png")
PURPLE_LASER= pygame.transform.rotate(pygame.transform.scale(PURPLE_LASER,(10,15)).convert_alpha(),-90)
# YELLOW_LASER = pygame.image.load ("fireball(1).jpg")
#Colours
white=(255,255,255)
black=(0,0,0)
blue=(0,0,255)
dark_orange=(255,140,0)
orange_red=(255,69,0)
red=(255,0,0)
turquoise=(64,224,208)
deep_blue=(0,191,255)
indigo=(75,0,130)
brown=(165,42,42)

lost_font = pygame.font.SysFont("comicsans", 60)
class Ship:
     laser_vel=0
     def __init__(self,x,y,health=100):
         self.x=x
         self.y=y
         self.health=health
         self.ship_img=None
         self.laser_img=None
         self.lasers=[]
         self.cool_down_counter = 0
     def draw(self,window):
          window.blit(self.ship_img,(self.x,self.y))
          # for laser in self.lasers:
          #      laser.draw(window)
     def shoot(self,velocity,cooldown_counter):
          if cooldown_counter==0:
               laser=Lasers(self.x-20,self.y,self.laser_img)
               self.lasers.append(laser)
          laser.draw(Screen)
          laser.move(velocity)
     def height(self):
          return self.ship_img.get_height()
     def width(self):
          return self.ship_img.get_width()
class Lasers:
     def __init__(self,x,y,img):
          self.x=x
          self.y=y
          self.img=img
          self.mask=pygame.mask.from_surface(self.img)
     def draw(self,win):
          win.blit(self.img,(self.x,self.y))
     def move(self,vel):
          self.y=vel
     def off_screen(self,height,vel):
          if vel >0:
               return self.y>=height 
          else:
               return self.y<0
     def collision(self,obj):
          return collide(self,obj)
class Player(Ship):
     laser_vel=-6
     def __init__(self, x, y, health=100):
         super().__init__(x, y, health=health)
         self.ship_img=YELLOW_SPACE_SHIP
         self.laser_img=RED_LASER
         self.mask=pygame.mask.from_surface(self.ship_img)
         self.max_health = health
class Enemy(Ship):
     color_map={"red":RED_SPACE_SHIP,"darkship":DARK_SPACE_SHIP,"darkship(2)":DARK_SPACE_SHIP_2}
     def __init__(self,x,y,color,health=100):
          super().__init__(x,y,health=health)
          self.ship_img=self.color_map[color]
          self.mask=pygame.mask.from_surface(self.ship_img)
          self.laser_img=BLUE_LASER
     def move(self,vel):
          self.y+=vel
def collide(obj1,obj2):
     offset_x=obj1.x-obj2.x
     offset_y=obj1.y-obj2.y
     return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))
def game_loop():
     enemies=[]
     wave_length=5
     level=0
     Live=5
     Screen.blit(Bgimg,(0,0))

     player=Player(300,400)
     
     Velocity_y=0
     Velocity_x=0
     while exit_game!=True:
          if Live==0:
               Screen.fill(black)
               Loose=lost_font.render("You Loose Press Enter to Re Start!",1,white)
               Screen.blit(Loose,(100,290))
               for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    if event.type==pygame.KEYDOWN:
                         if event.key==pygame.K_RETURN:
                              game_loop()
          else:
               if len(enemies)==0:
                    for i in range (wave_length):
                         enemy = Enemy(random.randint(50,Screen_width-100),random.randint(-1500,-100),random.choice(["red","darkship","darkship(2)"]))
                         enemies.append(enemy)
                    wave_length+=5
               Screen.blit(Bgimg,(0,0))
               for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    if event.type==pygame.KEYDOWN:
                         if event.key == pygame.K_RIGHT  :
                              Velocity_x+=VEL
                              Velocity_y=0
                         if event.key == pygame.K_LEFT:
                              Velocity_x-=VEL
                              Velocity_y=0
                         if event.key == pygame.K_UP:
                              Velocity_y-=VEL
                              Velocity_x=0
                         if event.key == pygame.K_DOWN:
                              Velocity_y+=VEL
                              Velocity_x=0
                         if event.key==pygame.K_SPACE:
                              pass
               player.x+=Velocity_x
               player.y+=Velocity_y
               if 0>player.x or 0>player.y:
                    player.x-=Velocity_x
                    player.y-=Velocity_y
               if player.x+player.width()>Screen_width or player.y+player.height()>Screen_height:
                    player.x-=Velocity_x
                    player.y-=Velocity_y
               for enemy in enemies:
                    enemy.draw(Screen)
                    enemy.move(enemy_Vel)
                    if enemy.y>Screen_width:
                         Live-=1
                         enemies.remove(enemy)
          
     
               player.draw(Screen)   
          pygame.display.update()
          clock.tick(fps)
          
game_loop()
     

