from pygame import *

window = display.set_mode((700,500))
display.set_caption('MAZE GAME')
background = transform.scale(image.load('background.jpg'),(700,500))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.Font(None,70)
win = font.render('You Win!',True,(255,215,0))
lose = font.render('You Lose!',True,(180,0,0))

game = True

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

    def movement_ctrl(self):

        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"

    def movement_ctrl(self):
        if self.rect.x <= 400:
            self.direction = "right"
        if self.rect.x >= 600:
            self.direction = "left"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width,wall_height):
        super().__init__()
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width,self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

player = GameSprite('hero.png',100,420,10)
monster= Enemy('cyborg.png',500,200,4)
goal = GameSprite('treasure.png',500,300,0)
w1 = Wall(154,205,50,100,20,450,10)
w2 = Wall(154,205,50,100,480,350,10)
w3 = Wall(154,205,50,100,20,10,380)

while game:
    window.blit(background,(0,0))
    player.reset()
    monster.reset()
    goal.reset()
    w1.draw_wall()
    w2.draw_wall()
    w3.draw_wall()

    if sprite.collide_rect(player,monster) or sprite.collide_rect(player,w1) or sprite.collide_rect(player,w2) or sprite.collide_rect(player,w3):
       finish = True
       window.blit(lose,(200,200))
       kick.play()

    if sprite.collide_rect(player,goal):
        game = True
        window.blit(win,(200,200))
        money.play()
        
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    player.movement_ctrl()
    monster.movement_ctrl()

    display.update()
    clock.tick(FPS)
