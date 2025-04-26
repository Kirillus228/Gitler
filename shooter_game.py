#Создай собственный Шутер!
# ! О НЕТ Я ЗАСТРЯЛ НА СВОЕЙ ТАРАНАЙКЕ СРЕДИ НЕПРОГЛЯДНОГО ЛЕСА
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image1, player_speed,  player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image1), (65, 70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_presset = key.get_pressed()         
        if keys_presset[K_RIGHT] and self.rect.x < 635:
            self.rect.x += 10  
        if keys_presset[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 10
    def fire(self):
        bullet = Bullet("bullet.jpg", 10, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        fire_sound.play()

lose = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0, 700)
            self.rect.y = 0
            global lose
            lose += 1
            
class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption("О НЕТ Я ЗАСТРЯЛ НА СВОЕЙ ТАРАНАЙКЕ СРЕДИ НЕПРОГЛЯДНОГО ЛЕСА")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

monsters = sprite.Group()
for i in range(4):
    monster = Enemy("ufo.png", randint(1, 5), randint(0, 700), 0)
    monsters.add(monster)

bullets = sprite.Group()

v1 = Player("rocket.png", 10, 350, 420)

font.init()
font2 = font.Font(None, 70)
win_label = font2.render('Не попуск', True, (255, 255, 255))
lose_label1 = font2.render('Попуск', True, (255, 255, 255))
game = True
clock = time.Clock()
mixer.init()
fon_sound = mixer.Sound("space.ogg")
mixer.music.load('space.ogg')
fon_sound.play()
mixer.music.load('fire.ogg')
fire_sound = mixer.Sound("fire.ogg")
FPS = 60
font = font.Font(None, 30)
win = 0
lives = 10
while game:
    window.blit(background, (0, 0))
    for ev in event.get():
        if ev.type == QUIT:
            game = False
        if ev.type == KEYDOWN:
            if ev.key == K_z:
                v1.fire()
    v1.update()
    v1.reset()
    bullets.draw(window)
    monsters.draw(window)
    for bullet in bullets:
        bullet.move()
    
    for monster in monsters:
        monster.update()
    collided1 = sprite.spritecollide(v1, monsters, True)
    for a in collided1:
        lives -= 1
        monster = Enemy("ufo.png", randint(1, 5), randint(0, 700), 0)
        monsters.add(monster)
    if lives == 0:
        window.blit(lose_label1, (290, 250))
        display.update()
        time.delay(3000)
        game = False
    collided = sprite.groupcollide(monsters, bullets, True, True)
    for enemy in collided:
        win  += 1
        monster = Enemy("ufo.png", randint(1, 5), randint(0, 700), 0)
        monsters.add(monster)
    if lose == 10:
        window.blit(lose_label1, (290, 250))
        display.update()
        time.delay(3000)
        game = False

    if win >= 20:
        window.blit(win_label, (290, 250))
        display.update()
        time.delay(3000)
        game = False     
    lose_point = font.render("D-ранк: " + str(lose), True, (255, 255, 255))
    win_point = font.render("P-ранк: " + str(win), True, (255, 255, 255))
    window.blit(lose_point,(0, 0))
    window.blit(win_point,(0, 20))
    live = font.render("V1: " + str(lives), True, (255, 255, 255))
    window.blit(live,(640, 0))

    
    display.update()
    clock.tick(FPS)