from levels import *
from game_class import Game

# Screen dimensions, all images should be reactive to this
X_RES = 1920
Y_RES = 1080

# Initialize the game screen
pygame.init()
screen = pygame.display.set_mode()
pygame.display.set_caption("Find the cow!")
clock = pygame.time.Clock()

# Create game object
game = Game()
game.load_level(1)

# Game loop
while True:
    clock.tick(60)
    for event in pygame.event.get():
        game.event_handler(event)

    if game.menu_flag:
        game.menu.draw(screen)

    else:
        game.update()
        game.draw(screen)

    pygame.display.update()

