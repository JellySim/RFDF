from sys import exit
from levels import *


class Game:
    def __init__(self, xres=1920, yres=1080):
        self.XRES = xres
        self.YRES = yres
        self.FRAME_RATE = 60
        self.level = 1

        # Sprite groups
        # **** TO DO - TIDY THIS MESS UP ****
        self.player = pygame.sprite.GroupSingle()
        self.player_tags = pygame.sprite.Group()
        self.overlay = pygame.sprite.GroupSingle()
        self.background = pygame.sprite.GroupSingle()
        self.flag = pygame.sprite.GroupSingle()
        self.guess_screen = pygame.sprite.GroupSingle()
        self.islands = pygame.sprite.Group()
        self.emitters = pygame.sprite.Group()
        self.enemy_territory = pygame.sprite.GroupSingle()
        self.exps = pygame.sprite.GroupSingle()
        self.yagis = pygame.sprite.Group()
        self.yagi_towers = pygame.sprite.Group()

        # Group for iterating
        self.sprite_groups = [self.player, self.player_tags, self.overlay, self.background, self.flag,
                              self.guess_screen, self.islands, self.emitters, self.enemy_territory,
                              self.exps, self.yagis, self.yagi_towers]

        # Create fog renderer
        self.fog = FogOfWar(self.XRES, self.YRES)

        # Menu sprite
        self.menu = pygame.sprite.GroupSingle(Menu())
        # Container for the current guess
        self.guess = None
        # Flags to see if we're on the score screen or the menu
        self.score_screen = False
        self.menu_flag = True


    def load_level(self, level):
        # Load in the level
        level = return_level(level, self.XRES, self.YRES)

        # Assign level sprites to the right groups
        self.player.add(level["player"])
        self.player_tags.add(level["player_omni"])
        self.islands.add(level["islands"])
        self.emitters.add(level["emitters"])

        if level['overlay']:
            self.overlay.add(level['overlay'])

        if level["enemy_territory"]:
            self.enemy_territory.add(level["enemy_territory"])

        self.exps.add(Explosion()) # Explosions don't change yet
        self.background.add(Background())  # Backgrounds don't change yet

    def reset(self):
        """Clear all of the sprites and reset the game state for the next level"""

        for moving_emitter in self.emitters:
            moving_emitter.emitter.stop_sound()

        self.fog = FogOfWar(self.XRES, self.YRES)
        self.guess = None
        self.score_screen = False

        for sprite in self.sprite_groups:
            sprite.empty()



    def update(self):
        # Update all the objects
        self.background.update()
        self.islands.update()
        self.emitters.update(self.player_tags.sprites()[0], self.yagis.sprites())
        self.player.update()
        self.player_tags.update(new_center=self.player.sprite.rect.center)
        self.yagi_towers.update()
        self.yagis.update()
        self.flag.update()

        if self.enemy_territory.__len__() >= 1:
            self.enemy_territory.update(self.player, self.exps)

        if self.exps.sprite.fire_flag:
            self.exps.update(self.player.sprite.rect.center)

    def draw(self, screen):
        # Draw the objects onto the screen (order matters)
        self.background.draw(screen)
        self.islands.draw(screen)
        self.player.draw(screen)
        self.emitters.draw(screen)
        if self.enemy_territory.__len__() >= 1:
            self.enemy_territory.draw(screen)

        if not self.score_screen:
            self.fog.draw(screen, self.player.sprite.rect.center)

        self.yagi_towers.draw(screen)

        for yagi in self.yagis:
            if yagi.selected:
                yagi.display(screen)

        for tag in self.player_tags:
            if tag.selected:
                tag.display(screen)

        if self.overlay:
            self.overlay.draw(screen)
        self.flag.draw(screen)
        self.guess_screen.draw(screen)
        if self.exps.sprite.fire_flag:
            self.exps.draw(screen)

    def event_handler(self, event):
        # ************** TO DO - TIDY THIS LOGIC ITS GROSS **********
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Sys exit to avoid screen refresh error

        if self.menu_flag and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.menu_flag = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()  # Sys exit to avoid screen refresh error

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.flag.__len__() >= 1:
            score = calc_score(self.emitters.sprites()[0].rect.center, self.guess)
            self.guess_screen.add(GuessScreen(score))
            self.score_screen = True

        # Checking mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # mouse_presses = [left, middle, right]
            mouse_presses = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            if mouse_presses[0] == 1 and self.score_screen:
                self.level += 1
                if self.level >= 5:
                    print("Thanks for playing!")
                    pygame.quit()
                    exit()

                self.reset()
                self.load_level(self.level)

            # Placing the Guess flag
            if mouse_presses[2] == 1:
                self.flag.empty()
                self.flag.add(GuessFlag(mouse_pos))
                self.guess = mouse_pos

            # Selecting sprites
            elif mouse_presses[0] == 1:
                # If we clicked on the player sprite (the boat)
                if self.player.sprite.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if not self.player.sprite.selected:
                        self.player.sprite.selected = True
                        self.player_tags.sprites()[0].selected = True
                        for sprite in self.yagis:
                            sprite.selected = False
                else:
                    # If we clicked on a yagi tower
                    for i in range(len(self.yagi_towers.sprites())):
                        self.yagis.sprites()[i].selected = False
                        if self.yagi_towers.sprites()[i].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                            self.yagis.sprites()[i].selected = True
                            self.player.sprite.selected = False
                            self.player_tags.sprites()[0].selected = False

        # Spawn trigger for yagi towers
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            if self.overlay.sprite.yagis > 0:
                mouse_pos = pygame.mouse.get_pos()

                for sprite in self.islands:
                    # Check to see if the mouse is over an islands
                    if (abs(mouse_pos[0] - sprite.rect.center[0]) <= 25) and \
                            (abs(mouse_pos[1] - sprite.rect.center[1]) <= 25):
                        self.yagi_towers.add(YagiTower(pygame.mouse.get_pos()))  # create a yagi sprite
                        self.yagis.add(Yagi(pygame.mouse.get_pos(), 30))  # add a yagi antenna
                        self.overlay.sprite.yagis -= 1
                        self.overlay.update()

            else:
                # Play a sound or something if we can't afford the yagi
                pass






