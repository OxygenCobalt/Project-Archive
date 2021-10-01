# Sprites.py
# All game objects [Such as the player, bullets] are in here.
import pygame
import public
import dictionaries

def on_split(self, group_a, group_b, vel_a, vel_b, vel_c):
    # Set up 3 seperate bullets with velocities and color given
    bullet_a = Bullet(self.rect.center, vel_a, self.alt_image, 'Bullet')
    bullet_b = Bullet(self.rect.center, vel_b, self.alt_image, 'Bullet')
    bullet_c = Bullet(self.rect.center, vel_c, self.alt_image, 'Bullet')

    # Add all bullets to the groups given [all_sprites/bullets]
    group_a.add(bullet_a, bullet_b, bullet_c)
    group_b.add(bullet_a, bullet_b, bullet_c)
    dictionaries.MEDIA['bullet_split_sound'].play()


class RectPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_bullets, direction, color, ability, *groups):
        super().__init__(*groups)
        self.image = dictionaries.PLAYER_MEDIA[color]['Image'] # Set player image from media dictionary
        self.color = dictionaries.PLAYER_MEDIA[color]['Color'] # Set player color [To stop players from killing themselves]
        self.bullet_image = dictionaries.PLAYER_MEDIA[color]['Bullet_Image'] # Set image for bullet [corresponding to color]
        self.fire_direction = direction
        self.params = dictionaries.PLAYER_MEDIA[color]['Parameters'] # Ability information [Image, name]
        self.ability = ability

        # More integral game variables
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(pos)
        self.health = 3
        self.enemy_bullets = enemy_bullets # Bullet group in order to detect for collided bullet
        self.toggle = False # Ties into game over screen

    def update(self):
        # Update position, based on velocity, and limit players to play area
        self.pos += self.vel
        self.rect.center = self.pos
        self.rect.clamp_ip(public.playarea)

        # Check for collided bullets
        collided = pygame.sprite.spritecollide(self, self.enemy_bullets, True)

        for bullet in collided:
            # Normal Bullet Case [1 damage]
            if bullet.type == 'Bullet':
                self.health -= 1
                dictionaries.MEDIA['hit_sound'].play()

                # Check for death
                if self.health == 0:
                    dictionaries.MEDIA['die_sound'].play()
                    self.kill()
                    self.toggle = True

            # Big Bullet case [2 damage]
            elif bullet.type == 'Big_Bullet':
                self.health -= 2
                dictionaries.MEDIA['hit_sound'].play()

                if self.health <= 0:
                    dictionaries.MEDIA['die_sound'].play()
                    self.kill()
                    self.toggle = True

            # Laser/Beam case [1 damage + An attempt to make knockback]
            elif bullet.type == 'Laser':
                self.health -= 1
                dictionaries.MEDIA['hit_sound'].play()

                if self.health <= 0:
                    dictionaries.MEDIA['die_sound'].play()
                    self.kill()
                    self.toggle = True
                else: # If not dead, deal knockback based on velocity of bullet
                    if bullet.vel[0] == 8 or -8 and bullet.vel[1] == 0:
                        self.pos[0] -= dictionaries.VELOCITY_VALUES['Convert']['Laser'][bullet.vel](bullet)
                    elif bullet.vel[1] == 8 or -8 and bullet.vel[0] == 0:
                        self.pos[1] -= dictionaries.VELOCITY_VALUES['Convert']['Laser'][bullet.vel](bullet)


# Basic bullet [All, is used for big_bullet]
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vel, image, bullet_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(vel)
        self.pos = pygame.math.Vector2(pos)
        self.toggle = False
        self.type = bullet_type

    def update(self):
        if self.toggle is False: # If bullet isnt already dead
            self.pos += self.vel
            self.rect.center = self.pos

            # If bullet has escaped boundaries of the play area [A.K.A hits a wall], remove self
            if not public.playarea.contains(self):
                self.kill()


# Beam [Red/Purple]
class Beam(pygame.sprite.Sprite):
    def __init__(self, pos, vel, color):
        super().__init__()
        self.color = color
        self.vel = vel
        self.image = dictionaries.VELOCITY_VALUES['Compare']['Laser_Image'][self.color][self.vel] # Use velocity to find orientation of image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.toggle = False
        self.type = 'Laser' # Type [To communicate to player]

    def update(self):
        if self.toggle is False:
            self.pos += self.vel
            self.rect.center = self.pos
            if not public.playarea.contains(self):
                self.kill()


# Split Bullet [Green/Yellow]
class SplitBullet(pygame.sprite.Sprite):
    def __init__(self, pos, vel, image, group_a, group_b, color):
        super().__init__()
        self.color = color
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.vel = vel
        self.pos = pygame.math.Vector2(pos)
        self.toggle = False
        self.type = 'Bullet'
        self.group_a = group_a
        self.group_b = group_b
        self.alt_image = dictionaries.PLAYER_MEDIA[self.color]['Bullet_Image']

    def update(self):
        if self.toggle is False:
            self.pos += self.vel
            self.rect.center = self.pos
            if not public.playarea.contains(self): # Again, check if bullet is in contact with the walls
                v_parameters = dictionaries.VELOCITY_VALUES['Convert']['Split_Bullet'][self.vel] # If so, fetch velocity parameters for the 3 bullets to be created
                on_split(self, self.group_a, self.group_b, *v_parameters) # Run On_Split using the velocity fetched
                self.kill()


# Reverse bullet [Grey/White]
class ReverseBullet(pygame.sprite.Sprite):
    def __init__(self, pos, vel, image, color):
        super().__init__()
        self.color = color
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.vel = vel
        self.pos = pygame.math.Vector2(pos)
        self.toggle = False
        self.type = 'Bullet'
        self.direction = dictionaries.VELOCITY_VALUES['Convert']['Reverse_Bullet']['Direction'][self.vel] # Find the specific velocity set needed to create the curve

    def update(self):
        if self.toggle is False:
            self.vel = dictionaries.VELOCITY_VALUES['Convert']['Reverse_Bullet'][self.color][self.direction](self) # Index the specific lambda function to change the velocity
            self.pos += self.vel
            self.rect.center = self.pos
            self.rect.center = self.pos
            if not public.playarea.contains(self):
                self.kill()


# Selector [For character select]
class Selector(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = dictionaries.MEDIA['selector']
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)

    def update(self, max, min):
        # Wraparound system

        self.rect.center = self.pos
        if self.pos[0] > max: # Overflow Case
            self.pos[0] = min
        elif self.pos[0] < min: # Underflow Case
            self.pos[0] = max


# Larger Selector [For mode select]
class SelectorBig(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = dictionaries.MEDIA['selectorbig']
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)

    def update(self):
        self.rect.center = self.pos

        # Different wraparound system that uses set values
        if self.pos[1] >= 500:
            self.pos[1] = 200
        elif self.pos[1] <= 100:
            self.pos[1] = 400

# OxygenCobalt