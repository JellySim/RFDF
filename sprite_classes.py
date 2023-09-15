import random
import pygame.draw
from utils import *
from os import getcwd


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, speed=3):
        super().__init__()
        fp = getcwd() + "\\Assets\\" + "Models\\boat\\"
        self.imgs = [
            pygame.image.load(fp + "ship1.png").convert_alpha(),
            pygame.image.load(fp + "ship3.png").convert_alpha(),
            pygame.image.load(fp + "ship5.png").convert_alpha(),
            pygame.image.load(fp + "ship7.png").convert_alpha(),
            pygame.image.load(fp + "ship9.png").convert_alpha(),
            pygame.image.load(fp + "ship11.png").convert_alpha(),
            pygame.image.load(fp + "ship13.png").convert_alpha(),
            pygame.image.load(fp + "ship15.png").convert_alpha()
        ]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.selected = True

    def player_input(self):
        # Map of keys and corresponding movements
        move_map = {pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0,  1),
                    pygame.K_LEFT: (-1,  0),
                    pygame.K_RIGHT: (1,  0)}

        # All the keys we have pressed since last frame (dict)
        keys = pygame.key.get_pressed()

        # create list of moves like: [(1, 0), (0, -1)]
        move = [move_map[key] for key in move_map if keys[key]]

        # Sum up the moves to give a total move
        summed_move = [sum(i) for i in zip(*move)]

        if summed_move and summed_move != [0, 0]:
            # We have to normalize the vector so that diagonal movement isn't faster
            move_vector = [i * self.speed for i in normalize(summed_move)]
            # Pick the right image
            self.animate(move_vector)

            # Apply the move vector it to our direction
            self.rect.move_ip(move_vector)

    def animate(self, move_vector):
        """function to animate the boat. pics the correct image depending upon which way the boat is moving"""
        if move_vector[0] == 0 and move_vector[1] < 0:
            # moving up
            self.image = self.imgs[0]

        elif move_vector[0] < 0 and move_vector[1] < 0:
            # moving up and left
            self.image = self.imgs[1]

        elif move_vector[0] < 0 and move_vector[1] == 0:
            # moving left
            self.image = self.imgs[2]

        elif move_vector[0] < 0 and move_vector[1] > 0:
            # down and left
            self.image = self.imgs[3]

        elif move_vector[0] == 0 and move_vector[1] > 0:
            # moving down
            self.image = self.imgs[4]

        elif move_vector[0] > 0 and move_vector[1] > 0:
            # down and right
            self.image = self.imgs[5]

        elif move_vector[0] > 0 and move_vector[1] == 0:
            # moving right
            self.image = self.imgs[6]

        elif move_vector[0] > 0 and move_vector[1] < 0:
            # moving up and right
            self.image = self.imgs[7]

        else:
            print("error in boat anim")

    def update(self):
        if self.selected:
            self.player_input()


class Omni(pygame.sprite.Sprite):
    def __init__(self, start_pos, offset=250):

        super().__init__()
        self.LINE_LENGTH = 280
        self.OFFSET = offset # the circular offset space around the boat sprite

        self.pos = start_pos
        self.end_pos = pygame.math.Vector2(self.pos[0] + self.LINE_LENGTH, self.pos[1])

        self.selected = True

    def move(self, new_rect_center):
        self.pos = new_rect_center

    def display(self, screen):
        self.end_pos = pygame.math.Vector2(self.pos[0] + self.LINE_LENGTH, self.pos[1])

        for i in range(0, 360):
            # Only draw every sixth line
            if i%6 != 0:
                continue

            rot_end = pygame.math.Vector2.rotate((self.end_pos - self.pos), i)
            rot_end += self.pos

            offset = pygame.math.Vector2(self.pos)
            offset = offset.move_towards(rot_end, self.OFFSET)

            colour = (255, 90, 54)
            pygame.draw.line(screen, colour, offset, (rot_end.x, rot_end.y), width=2)

    def update(self, new_center):
        self.move(new_center)


class Yagi(pygame.sprite.Sprite):
    def __init__(self, start_pos, angle, speed=0.5):
        super().__init__()
        self.speed = 3
        self.start_pos = start_pos
        self.LINE_LENGTH = 1200

        self.end_pos = pygame.math.Vector2(self.start_pos[0] + self.LINE_LENGTH, self.start_pos[1])
        self.start_vector = pygame.math.Vector2(start_pos)
        self.selected = False

        # Bit of math to figure out the end points of our two lines
        self.angle_start = 0
        self.return_angle = 0 # The angle we pass to the emitters

    def display(self, screen):
        for i in range(-9, 9):

            rot_end = pygame.math.Vector2.rotate((self.end_pos - self.start_pos), (self.angle_start + i))
            rot_end += self.start_pos

            colour = (255, 90, 54)
            pygame.draw.line(screen, colour, self.start_pos, (rot_end.x, rot_end.y), width=2)

    def player_input(self):
        # Map of keys and corresponding movements
        if self.selected:
            move_map = {pygame.K_LEFT: (-1,  0),
                        pygame.K_RIGHT: (1,  0)}

            # All the keys we have pressed since last frame (dict)
            keys = pygame.key.get_pressed()

            # create list of moves like: [(1, 0), (0, -1)]
            move = [move_map[key] for key in move_map if keys[key]]

            if move == [(1, 0)]:
                self.angle_start += 0.5
            elif move == [(-1, 0)]:
                self.angle_start -= 0.5

            if self.angle_start % 360 == 0:
                self.angle_start = 0

    def calc_return_angle(self):
        if -180 < self.angle_start <= 180:
            self.return_angle = self.angle_start

        elif self.angle_start > 181:
            self.return_angle = (360 - (self.angle_start% 360)) * -1

        elif self.angle_start <= -180:
            self.return_angle = ((self.angle_start % -360) + 360) * -1

        else:
            print(f"error, start angle of {self.angle_start} and return angle of {self.return_angle}")

    def update(self):
        # Only does stuff if it's selected
        if self.selected:
            self.player_input()
            self.calc_return_angle()


class YagiTower(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()

        fp = getcwd() + "\\Assets\\" + "Models\\stand_in_tower.png"
        self.image = pygame.image.load(fp)
        size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (size[0]/3, size[1]/3))
        self.rect = self.image.get_rect(center=start_pos)


class Background(pygame.sprite.Sprite):
    def __init__(self, start_pos=(0,0), x_res=1920, y_res=1080,
                 fp=getcwd() + "\\Assets\\" + "Models\\Water\\Water.jpg"):
        super().__init__()
        if fp:
            self.image = pygame.image.load(fp).convert_alpha()
            self.image = pygame.transform.scale(self.image, (x_res, y_res))
            self.rect = self.image.get_rect(topleft=start_pos)
        else:
            "simple image for testing"
            self.image = pygame.Surface((x_res, y_res))
            self.image.fill("Blue")
            self.rect = self.image.get_rect(topleft=start_pos)

        anim_fp = getcwd() + "\\Assets\\" + "\\Models\\Water\\Caustics\\"

        self.start_pos=start_pos
        self.anim = pygame.image.load(anim_fp + "caust_003.png").convert_alpha()
        self.anim = pygame.transform.scale(self.anim, (x_res, y_res))
        self.anim.set_alpha(40)

        self.image.blit(self.anim, self.anim.get_rect(topleft=self.start_pos))


class Island(pygame.sprite.Sprite):
    def __init__(self, start_pos, fp=None, x_res=1920,):
        super().__init__()
        if fp is None:
            fp = getcwd() + "\\Assets\\" +\
                 "islands\\" +\
                 "isle_" + str(random.randint(1, 23)) + ".png"

        self.image = pygame.image.load(fp).convert_alpha()
        self.image = pygame.transform.scale(self.image, (x_res/4, x_res/4))
        self.rect = self.image.get_rect(center=start_pos)


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fp = getcwd() + "\\Assets\\"

        self.countdown = pygame.mixer.Sound(
            fp + "Sounds\\explosion_countdown.mp3")
        self.countdown.set_volume(0.6)
        self.explosion_sound = pygame.mixer.Sound(
            fp + "\\Sounds\\explosion_sound.mp3")
        self.explosion_sound.set_volume(0.6)

        self.imgs = [
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c1.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c2.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c3.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c4.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c5.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c6.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c7.png").convert_alpha(),
            pygame.image.load(fp + "\\Models\\explosion1\\explosion-c8.png").convert_alpha(),
        ]

        self.fire_flag = False
        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        self.anim_timer = 0

    def play_countdown(self):
        self.countdown.play()

    def play_explosion(self):
        self.explosion_sound.play()

    def stop_countdown(self):
        self.countdown.stop()

    def update(self, pos):
        self.rect.center = pos
        if self.anim_timer >= 8:
            self.fire_flag = False

        else:
            selector = int(self.anim_timer//1)
            self.image = self.imgs[selector]

        self.anim_timer += 0.2


class EmittingSprite(pygame.sprite.Sprite):
    """
    A sprite with movement and animations that has an emitter attached to it
    """
    def __init__(self, img_file, sound_file, start_pos, control_points=None, scale=None, speed=1, path_reverse=True):
        super().__init__()
        self.image = pygame.image.load(img_file)

        if scale:
            self.image = pygame.transform.scale(self.image, scale)

        self.start_pos = start_pos
        self.speed = speed # Movement speed if the emitter is a moving emitter, N points per frame, supports values
                           # less than 1

        self.construct_path(control_points)
        self.move_counter = 0
        self.path_reverse = path_reverse # If the path should be reversed after the sprite has moved along it
        self.rect = self.image.get_rect(center=start_pos)
        self.emitter = Emitter(sound_file, start_pos)

        # First run flag
        self.start = True

    def move(self):
        index = int(self.move_counter//1)

        self.rect.center = self.path[index]
        self.move_counter += self.speed

        if (self.move_counter//1) >= len(self.path):
            self.move_counter = 0

            # Reverse the path if it's flagged to do so
            if self.path_reverse:
                self.path = self.path[::-1]

    def construct_path(self, control_points):
        if control_points:
            x_bez, y_bez = bezier_curve(control_points, 500)
            self.path = [i for i in zip(x_bez, y_bez)]

        else:
            self.path = None

    def update(self, omnis, yagis):
        if self.start:
            self.emitter.start_game()
            self.start = False

        # Move if applicable
        if self.path:
            self.move()

        self.emitter.move(self.rect.center)
        self.emitter.update(omnis, yagis)


class Emitter(pygame.sprite.Sprite):
    def __init__(self, sound_file, start_pos):
        super().__init__()
        self.pos = start_pos

        # Sounds
        self.emitting_sound = pygame.mixer.Sound(sound_file)
        self.emitting_sound.set_volume(0.5)

        self.static = pygame.mixer.Sound(getcwd() + "\\Assets\\" + "Sounds\\radio_noise.mp3")
        self.static_vol = 0.1
        self.static.set_volume(self.static_vol)

        self.og_vol = self.emitting_sound.get_volume()
        self.curr_vol = 0
        self.yagi_vols = []
        self.omni_vol = 0
        self.emitting_sound.set_volume(self.curr_vol)

        self.curr_channel = None

    def start_game(self):
        self.emitting_sound.play(loops=1000)
        self.static.play(loops=20)

    def stop_sound(self):
        self.static.stop()
        self.emitting_sound.stop()

    def yagi_distance(self, yagis):
        """calcs the distance from the yagi antenna and the direction the antenna is currently pointing"""
        distances = []
        for yagi in yagis:
            # If we haven't selected the yagi just continue
            if not yagi.selected:
                distances.append((99999, 99999, 99999))
                continue

            # First, find the shortest distance between yagi line (the main line of the yagi antenna) and the
            # emitter. This will be miss_d
            v1 = pygame.math.Vector2(self.pos)
            v2 = pygame.math.Vector2(yagi.start_pos)
            d = distance(self.pos, yagi.start_pos)

            ideal_angle = pygame.math.Vector2()
            ideal_angle = ideal_angle.angle_to(v1 - v2)
            miss_angle = abs(yagi.return_angle - ideal_angle)

            if miss_angle >= 90:
                # If the yagi is pointing more than 90 degrees away from the emitter, put in a big number
                distances.append((99999, 99999, 99999))
                continue

            miss_angle_rads = miss_angle * math.pi/180
            miss_d = d * math.sin(miss_angle_rads) # the line distance between the emitter and the yagi line

            distances.append((d, miss_d, miss_angle))

        self.yagi_vols = distances # will be converted to volumes with yagi_volume()

    def omni_volume(self, omni):
        """calcs the volume of the emitter given the distance from the omni antenna"""
        # If we haven't selected the omni
        if not omni.selected:
            self.omni_vol = 0

        else:
            d = distance(self.pos, omni.pos)
            if d > 1000:
                self.omni_vol = 0
            else:
                self.omni_vol = min(100/(0.3*d + d**1.52 + 0.01), 1)

    def yagi_volume(self):
        """calc the volume of the emitter given the distance from the emitter and the yagi antenna and the
         distance from the central beam of the yagi"""
        vols = []
        for d, miss_d, miss_angle in self.yagi_vols:
            if miss_d > 10000:
                vols.append(0)
            else:
                # We want the yagi beam to fan out like a torch beam, so the strength of the sound is a function
                # of the distance from the yagi itself, and the distance from the central beam line of the yagi
                # In the fn below:
                # min(x, 1)      1 is the maximum volume we want
                # 100            100 pixels is the region in which the volume will be at 1 (so the maxiumum accuracy in
                #                pixels)
                # miss_angle*2.5 Modulates the volume by how oblique the emitter is to the antenna
                # 0.9*d          Gives a volume dropoff for emitters further away from the antenna
                #                straight line distance)
                # miss_d**1.5    Gives an exponential drop off from the center of the antenna line

                vols.append(
                    min(
                        (100 - miss_angle*2.5) / (0.9*d + miss_d**1.5 + 0.01),
                        1)
                )

        self.yagi_vols = vols

    def calc_curr_vol(self):
        """calculates the current emitting volume given the yagi volumes and the omni volume"""
        # wrangle the vols
        vols = [i for i in self.yagi_vols]
        vols.append(self.omni_vol)

        self.curr_vol = min(max(vols) + (sum(vols)/len(vols)), 1)

    def play_sound(self):
        self.curr_channel = self.emitting_sound.play()

    def move(self, coord):
        self.pos = coord

    def update(self, omni_collider, yagis):
        # Calculate volumes
        self.omni_volume(omni_collider)
        self.yagi_distance(yagis)
        self.yagi_volume()
        self.calc_curr_vol()

        # Set volumes
        self.emitting_sound.set_volume(self.curr_vol)
        self.static.set_volume(self.static_vol - self.curr_vol)


class LightGlow:
    def __init__(self, radius=150, glow=11, layers=25):
        super().__init__()
        self.radius = radius
        self.glow = glow
        self.layers = layers

        self.image = self.generate_glow()

    def generate_glow(self):
        # Generate square surface of size 2* radius
        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # restrict glow
        glow = pygame.math.clamp(self.glow, 0, 255)
        for i in range(self.layers):
            k = i * glow
            k = int(pygame.math.clamp(k, 0, 255))
            pygame.draw.circle(
                surf, (k, k, k), surf.get_rect().center, self.radius - i * 3
            )

        # return the surf
        return surf

    def update_glow(self):
        self.glow += 1
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        layers = 25
        self.glow = pygame.math.clamp(self.glow, 0, 255)
        for i in range(layers):
            k = i * self.glow
            k = int(pygame.math.clamp(k, 0, 255))
            pygame.draw.circle(
                self.surf, (k, k, k), self.surf.get_rect().center, self.radius - i * 3
            )


class FogOfWar:
    def __init__(self, x_res=1920, y_res=1080):
        self.surf = pygame.Surface((x_res, y_res))
        self.light = LightGlow()
        self.cell_size = 8*2
        self.grid = [
            [0 * random.random() for _ in range(x_res // self.cell_size)]
            for _ in range(y_res // self.cell_size)
        ]

    def draw(self, surf: pygame.Surface, pos):
        # self.light.update_glow()
        size = self.cell_size

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                k = self.grid[row][col]
                if k > 0:
                    k -= 0.1
                    self.grid[row][col] = pygame.math.clamp(k, 25, 255)

                # I turned this stuff off to save on performance

                # k = int(self.grid[row][col])
                # center = (col * size + size // 2, row * size + size // 2)

                # if distance(center, pos) < self.light.radius:
                #     color = 55
                #     self.grid[row][col] = color
                #     k = color
                #     k -= (11 - self.light.glow) * 2
                # k = pygame.math.clamp(k, 0, 255)
                # pygame.draw.rect(self.surf, (k, k, k), (col * size, row * size, size, size))

        self.surf.blit(
            self.light.image,
            self.light.image.get_rect(center=pos),
            special_flags=pygame.BLEND_RGBA_MAX,
        )

        surf.blit(self.surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class EnemyTerritory(pygame.sprite.Sprite):
    def __init__(self, x_res, y_res, fp):
        super().__init__()
        # colour and shape the describes enemy territory
        self.x_res = x_res
        self.y_res = y_res
        self.enemy_colour = (237, 71, 71, 128)
        self.image = pygame.image.load(fp).convert_alpha()
        self.rect = self.image.get_rect()

        self.make_alpha()

        # collision mask and collision flags
        self.mask = pygame.mask.from_surface(self.image)
        self.collision_flag = False
        self.collision_timer = 0
        self.kill_player_flag = False

    def make_alpha(self):
        for x in range(self.x_res):
            for y in range(self.y_res):
                pixel = self.image.get_at((x, y))
                if (pixel[0] >= 200 and pixel[1] >= 200) or pixel[3] == 0:     # If it's white or transparent
                    self.image.set_at((x, y), (255, 255, 255, 0))
                else:
                    self.image.set_at((x, y), self.enemy_colour)

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, (0, 0))

    def check_collision(self, player, explosion):
        """
        Checks for collisions between the enemy territory and the player
        """

        if pygame.sprite.collide_mask(player.sprite, self) and not \
                self.collision_flag and not player.sprite.dead:
            # If it's the first time we hit
            if not self.collision_flag:
                explosion.sprite.countdown.play()
                self.collision_timer = pygame.time.get_ticks()
                self.collision_flag = True

        elif pygame.sprite.collide_mask(player.sprite, self) and self.collision_flag:
            if (pygame.time.get_ticks() - self.collision_timer) > (explosion.sprite.countdown.get_length() * 1000):
                # Create explosion sprite, play the sound
                player.sprite.dead = True
                explosion.sprite.explosion_sound.play()
                self.kill_player_flag = True
                self.collision_flag = False

        elif self.collision_flag and not pygame.sprite.collide_mask(player.sprite, self):
            explosion.sprite.countdown.stop()
            self.collision_flag = False

    def update(self, player, explosion):
        self.check_collision(player, explosion)

        if self.kill_player_flag:
            explosion.sprites()[0].fire_flag = True


class Overlay(pygame.sprite.Sprite):
    def __init__(self, yagi_count, xres, yres):
        super().__init__()
        self.image = pygame.image.load(getcwd() + "\\Assets\\" + "Models\\overlay.png")
        self.rect = self.image.get_rect(midtop=(xres/2, 0))
        self.yagis = yagi_count
        self.font = pygame.font.SysFont('helveticaltstdblk', 80)
        self.text = self.font.render(f"{self.yagis}", False, (0, 0, 0))

        self.image.blit(self.text, (self.image.get_size()[0] / 3, self.image.get_size()[1] / 3.5))

    def update(self):
        self.image = pygame.image.load(getcwd() + "\\Assets\\" + "Models\\overlay.png")
        if self.yagis > 0:
            self.text = self.font.render(f"{self.yagis}", False, (0, 0, 0))
        else:
            self.text = self.font.render(f"{self.yagis}", False, (255, 0, 0))
        self.image.blit(self.text, (self.image.get_size()[0]/3, self.image.get_size()[1]/6))


class GuessFlag(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        sheet = SpriteSheet(getcwd() + "\\Assets\\" + "Models\\flag_animation.png")
        sprite_size = (0, 0, 60, 60)

        self.images = sheet.load_strip(sprite_size, 5, colorkey=(255, 255, 255))

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (start_pos[0] - 9, start_pos[1])

        self.anim_timer = 0
        self.selector = self.anim_timer//1

    def update(self):
        if self.anim_timer >= 5:
            self.anim_timer = 0

        if self.selector != int(self.anim_timer//1):
            self.selector = int(self.anim_timer//1)
            self.image = self.images[self.selector]

        self.anim_timer += 0.08


class GuessScreen(pygame.sprite.Sprite):
    def __init__(self, guess):
        super().__init__()
        self.image = pygame.image.load(getcwd() + "\\Assets\\" + "Models\\scroll.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1500, 1300))
        self.rect = self.image.get_rect()
        self.rect.midtop = (1920/2, -100)

        self.font = pygame.font.SysFont('helveticaltstdblk', 30)
        self.text1 = self.font.render(f"You're {guess} from the target!", False, (0, 0, 0))
        self.text2 = self.font.render(f"Good/Bad Job!", False, (0, 0, 0))

        self.retry_text = self.font.render(f"Next", False, (0, 0, 0))
        self.retry_button = pygame.surface.Surface((150, 80))
        self.retry_button.fill((252, 247, 165))
        self.retry_button.blit(self.retry_text, (36, 27))
        pygame.draw.rect(self.retry_button, (122, 62, 18), self.retry_button.get_rect(), width=2)

        self.image.blit(self.retry_button, (self.rect.center[0] - 320, self.rect.center[1] + 180))

        self.image.blit(self.text1, (self.rect.center[0] - 450, self.rect.center[1]-150))
        self.image.blit(self.text2, (self.rect.center[0] - 450, self.rect.center[1]-100))


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(getcwd() + "\\Assets\\" + "Models\\title.png")
        self.rect = self.image.get_rect(topleft=(0,0))
        self.font = pygame.font.SysFont('helveticaltstdblk', 50)
        self.text1 = self.font.render(f"<< Press Space to Start >>", False, (0, 0, 0))
        self.text1.get_rect(center=(0,0))

        self.image.blit(self.text1, ((self.image.get_width() - self.text1.get_width()) / 2,
                                     950))
                                    #(self.image.get_height() - self.text1.get_height()) / 2 + 300))





