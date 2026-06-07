from pygame import *
from random import randint
from time import time as timesec
#Modificaicones
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self, hitbox = False):
        window.blit(self.image, (self.rect.x, self.rect.y))
        if hitbox: draw.rect(window, (255,0,0), self.rect, 1)

class DinamicSprites(GameSprite):
  def __init__(self, player_image, player_x, player_y, size_x, size_y, speed = 0):
     super().__init__(player_image, player_x, player_y, size_x, size_y)
     self.speed = speed

# clase del jugador principal
class Player(DinamicSprites):
  def move(self, speedx):
    self.speed = speedx
    
  def update(self):
    self.rect.x += self.speed
  

class Ball(DinamicSprites):
  def update(self):
    global lost

    if self.rect.top >= 500:
      self.rect.x = randint(0,420)
      self.rect.y = -45
      self.speed = randint(1,6)
      lost += 1
       

init()
window = display.set_mode((700,500))
display.set_caption("Tirador")
background = (127, 233, 240)

clock = time.Clock()
lost = 0

ball = Ball("football.png", 250, 200, 50, 50, 1)
player1 = Player("paleta.png", 10, 100, 25, 180, 2)
player2 = Player("paleta.png", 665, 100, 25, 180, 2)

txt_font = font.Font(None, 40)
score = 0
message_score = txt_font.render("Puntaje: " + str(score), True, (255,255,255))
message_lost = txt_font.render("Fallos: " + str(lost), True, (255,255,255))

victory = font.Font(None, 80).render('¡¡Ganaste!!', True, (0,255,0))
defeat = font.Font(None, 80).render('¡¡Perdiste!!', True, (255,0,0))


time_shot = timesec()
run = True 
while run:
  for e in event.get():
    if e.type == QUIT:
      run = False

  
  if lost < 4 and score < 10:

    window.fill(background)
    ball.update()
  message_lost = txt_font.render("Fallos: " + str(lost), True, (255,255,255))
  message_score = txt_font.render("Puntaje: " + str(score), True, (255,255,255))
  

  ball.reset()
  player1.reset()
  player2.reset()

  window.blit(message_score, (50,10))
  window.blit(message_lost, (50,40))
  if score >= 10:
    window.blit(victory, (200, 150))
  elif lost >= 4:
    window.blit(defeat, (200, 150))
    
  
  display.update()
  clock.tick(40)
