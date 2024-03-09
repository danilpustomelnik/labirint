#створи гру "Лабіринт"!
from typing import Any
from pygame import*


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[K_UP] and  self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and  self.rect.y < 450:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 550:
            self.direction = 'right'
        if self.rect.x >= 700:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed 
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

window = display.set_mode ((700,500))
display.set_caption('labirint')
background = transform.scale(image.load('background.jpg'), (700, 500))

game =True
clock = time.Clock()
FPS = 60

finish=False

font.init()
font=font.Font(None, 70)
win = font.render('YOU WIN!', True, (255,215,0))
lose=font.render('YOU LOSE!', True, (180,0,0))

mixer.init()
mixer.music.load('zvuki-na-ulice-goroda.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')


player=Player('hero.png', 50,400, 6)
zlodey=Enemy('cyborg.png', 700,300, 3)
moneti=GameSprite('treasure.png', 600, 400, 0)

w1 = Wall(0, 255, 0, 100, 20, 450, 10)
w2 = Wall(0, 255, 0, 150, 100, 10, 1000)
w3 = Wall(0, 255, 0, 250, 20, 10, 400)
w4 = Wall(0, 255, 0, 350, 100, 10, 1000)
w5 = Wall(0, 255, 0, 450, 20, 10, 400)
w6 = Wall(0, 255, 0, 550, 100, 10, 1000)
while game:
    for e in event.get():
        if e.type == QUIT:
            game=False

    if finish!=True:
        window.blit(background,(0,0))
        player.reset()
        player.update()
        zlodey.reset()
        zlodey.update()
        moneti.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()

        if (sprite.collide_rect(player, w1)
            or sprite.collide_rect(player, w2)
            or sprite.collide_rect(player, w3)
            or sprite.collide_rect(player, w4)
            or sprite.collide_rect(player, w5)
            or sprite.collide_rect(player, w6)):
                kick.play()
                player.rect.x=50
                player.rect.y=400

        if sprite.collide_rect(player, zlodey):
            window.blit(lose, (200, 200))
            player.rect.x=50
            player.rect.y=400
            kick.play()
            finish=True

        if sprite.collide_rect(player, moneti):
            window.blit(win, (200, 200))
            money.play()
            player.rect.x=50
            player.rect.y=400
            finish=True

    display.update()
    clock.tick(FPS)