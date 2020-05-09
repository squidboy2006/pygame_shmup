# art by kenney.ln


import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')


WIDTH = 450
HEIGHT = 600
FPS = 60
POWERUP_TIME = 3000

# colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (125, 0, 255) 
GRAY = (125, 125, 125)
ORANGE = (255, 125, 0)
DARK_GRAY = (50, 50, 50)
SPACE_GRAY = (45, 50, 65)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 10
    BAR_HEIGHT = 550
    fill = (pct / 100) * BAR_HEIGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, BAR_LENGTH, fill)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("shmup!")
clock = pygame.time.Clock()

# player sprite
def draw_lives(surf, x ,y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.radius = 20
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 350
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
  
    def update(self): 
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    
    def hide(self): 
        # hides player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 10)  
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect() 
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
      

   
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
             self.kill()




class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'damage_shield'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
             self.kill()




class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        if self.image == explosion_anim['player']:
            self.frame_rate = 100
        else:
            self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




def show_go_screen():
    screen.fill(SPACE_GRAY)
    draw_text(screen, 'shmup', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Arrow keys move, spacebar to fire', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'press a key to begin', 18, WIDTH / 2, HEIGHT * 3 / 4)
    draw_text(screen, str(score), 18, WIDTH / 2, 100) 
    pygame.display.flip()
    waiting = True
    while waiting == True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False




#load game graphics
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med3.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big2.png', 'meteorBrown_big4.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 
                'meteorBrown_small2.png','meteorBrown_tiny1.png'] 
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert() )



 
# load game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'shieldPowerup.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'gunPowerup.wav'))
damage_shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'Powerdown.wav'))
explosion_sounds = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(2):
    filename = 'smokeOrange{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'smokeWhite{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_silver.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['damage_shield'] = pygame.image.load(path.join(img_dir, 'shield_bronze.png')).convert()



score = 0
game_over = True
running = True
while running:
    if game_over == True:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group() 
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player ()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0

    clock.tick(FPS)

    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update 
    all_sprites.update()

    # check for collisions 
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for collision in hits:
        score += 60 - collision.radius 
        random.choice(explosion_sounds).play()
        expl = Explosion(collision.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.92:
            pow = Powerup(collision.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
    
    #check if player collides with a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for collision in hits:
        if collision.type == 'shield':
            player.shield += random.randrange(8,25)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if collision.type == 'damage_shield':
            player.shield -= random.randrange(8, 25)
            damage_shield_sound.play()
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                random.choice(explosion_sounds).play()
                player.hide()
                player.lives -= 1
                player.shield = 100
        if collision.type == 'gun':
            player.powerup()
            power_sound.play()


    # check if meteor hits the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for collision in hits:
        player.shield -= (collision.radius * 2) + 5
        random.choice(explosion_sounds).play()
        expl = Explosion(collision.rect.center, 'sm')
        all_sprites.add(expl)
        newmob() 
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            random.choice(explosion_sounds).play()
            player.hide()
            player.lives -= 1
            player.shield = 100

    #if player has died and explosion is finished
    if player.lives == 0:
        if not death_explosion.alive():
            game_over = True
            

    # Draw 
    screen.fill(SPACE_GRAY)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10) 
    draw_shield_bar(screen, 435, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    # after drawing everything, flip display
    pygame.display.flip()


pygame.quit