from pygame import *
from random import shuffle
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
  def move(self, speedy):
    self.speed = speedy
    
  def update(self):
    self.rect.y += self.speed
  

class Ball(DinamicSprites):

  def aleatorio(self):
    velocidad = [5,-5]
    shuffle(velocidad)
    self.speedx = velocidad[0]
    shuffle(velocidad)
    self.speedy = velocidad[0]

  def update(self, p1, p2):

    self.rect.x += self.speedx
    self.rect.y += self.speedy

    if self.rect.top <= 0 or self.rect.bottom >= 500:
      self.speedy *= -1

    if self.rect.colliderect(p1) or self.rect.colliderect(p2):
      self.speedx *= -1

    elif self.rect.left >=  700:
      print("Jugador1 uno anoto un punto")
      self.rect.x = 250
      self.rect.y = 200
      self.aleatorio()

    elif self.rect.right <=  0:
      print("Jugador2 uno anoto un punto")
      self.rect.x = 250
      self.rect.y = 200
      self.aleatorio()
       

init()
window = display.set_mode((700,500))
display.set_caption("Tirador")
background = (127, 233, 240)

clock = time.Clock()
lost = 0

ball = Ball("football.png", 250, 200, 50, 50, 1)
ball.aleatorio()
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

  

  keys_presed = key.get_pressed()
  if keys_presed[K_w] and player1.rect.top > 0: player1.move(-5)
  elif keys_presed[K_s] and player1.rect.bottom < 500: player1.move(5)
  else: player1.move(0)
  if keys_presed[K_UP] and player2.rect.top > 0: player2.move(-5)
  elif keys_presed[K_DOWN] and player2.rect.bottom < 500: player2.move(5)
  else: player2.move(0)

  message_lost = txt_font.render("Fallos: " + str(lost), True, (255,255,255))
  message_score = txt_font.render("Puntaje: " + str(score), True, (255,255,255))
  window.fill(background)
  ball.update(player1.rect, player2.rect)
  player1.update()
  player2.update() 

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
