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
  
  def fire(self):
    global bullets
    bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20)
    bullet.rect.centerx = self.rect.centerx
    bullets.add(bullet)
     
# clase del jugador principal
class Enemy(DinamicSprites):
  def update(self):
    global lost
    self.rect.y += self.speed
    if self.rect.top >= 500:
      self.rect.x = randint(0,420)
      self.rect.y = -45
      self.speed = randint(1,6)
      lost += 1
      
class Bullet(DinamicSprites):
  def __init__(self, player_image, player_x, player_y, size_x, size_y):
    super().__init__(player_image, player_x, player_y, size_x, size_y, -15)
    
  def update(self):
    self.rect.y += self.speed
         


init()
window = display.set_mode((700,500))
display.set_caption("Tirador")
background = GameSprite("galaxy.jpg", 0, 0 ,700, 500)
clock = time.Clock()
lost = 0

#Sprites
player = Player("rocket.png", 300 , 420, 45, 70)
monsters = sprite.Group()

for i in range(5):
  monsters.add(Enemy("ufo.png", randint(0,630), 0, 70, 45, randint(1,4))) 

bullets = sprite.Group()

txt_font = font.Font(None, 40)
score = 0
message_score = txt_font.render("Puntaje: " + str(score), True, (255,255,255))
message_lost = txt_font.render("Fallos: " + str(lost), True, (255,255,255))

victory = font.Font(None, 80).render('¡¡Ganaste!!', True, (0,255,0))
defeat = font.Font(None, 80).render('¡¡Perdiste!!', True, (255,0,0))

mixer.init()
mixer.music.load("./music_background.mp3")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
explosion = mixer.Sound("explosion.wav")

time_shot = timesec()
run = True 
while run:
  for e in event.get():
    if e.type == QUIT:
      run = False
#    if e.type == KEYDOWN:
#      if e.key == K_SPACE: bullets.add(player.fire())
  
  if lost < 4 and score < 10:
    keys_presed = key.get_pressed()
    if (keys_presed[K_LEFT] or keys_presed[K_a]) and player.rect.left > 0: player.move(-5)
    elif (keys_presed[K_RIGHT] or keys_presed[K_d]) and player.rect.right < 700: player.move(5)
    else: player.move(0)
    if keys_presed[K_SPACE]: 
      if timesec() - time_shot > 0.5:
        fire.play() 
        player.fire()
        time_shot = timesec()
    
    bullets.update()
    player.update()
    monsters.update()
  message_lost = txt_font.render("Fallos: " + str(lost), True, (255,255,255))
  message_score = txt_font.render("Puntaje: " + str(score), True, (255,255,255))
  
  for enemy_defeat in sprite.groupcollide(monsters, bullets, True, True):
    explosion.play()
    score += 1
    monsters.add(Enemy("ufo.png", randint(0,630), 0, 70, 45, randint(1,4)))

  if len(sprite.spritecollide(player, monsters, True)) > 0:
    explosion.play()
    lost = 4
  
  
  background.reset()
  bullets.draw(window)
  player.reset()
  monsters.draw(window)
  window.blit(message_score, (50,10))
  window.blit(message_lost, (50,40))
  if score >= 10:
    window.blit(victory, (200, 150))
  elif lost >= 4:
    window.blit(defeat, (200, 150))
    
  
  display.update()
  clock.tick(40)