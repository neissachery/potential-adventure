import pygame
import sys
import random
from pygame.locals import *
FPS = 32
window_width = 600
window_height = 499
window = pygame.display.set_mode((window_width,window_height))
elevation = window_height*0.8
game_images = {}

buzy_bee = 'BuzzyBee/bee2.png'
background = 'BuzzyBee/background1.jpg'
pipe_image = 'BuzzyBee/pipesingle4.png'
floor = 'BuzzyBee/bricj.jpg'

def beegame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width + 300 - mytempheight + (window_width / 2),
         'y': second_pipe[1]['y']},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width + 200 - mytempheight + (window_width / 2),
         'y': second_pipe[0]['y']},
    ]

    bee_velocity_y= -9
    bee_Max_Vel_Y = 10
    bee_Min_Vel_Y = -8
    beeAccY= 1
    pipeVelX = -4
    bee_fly_velocity = -8
    bee_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bee_velocity_y = bee_fly_velocity
                    bee_flew = True
        game_over = isGameOver(horizontal,vertical,up_pipes,down_pipes)
        if game_over:
            return
        playerMidPos = horizontal + game_images['bee'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your your_score is {your_score}")
        if bee_velocity_y < bee_Max_Vel_Y and not bee_flapped:
            bee_velocity_y += beeAccY

        if bee_flapped:
            bee_flapped = False
        playerHeight = game_images['bee'].get_height()
        vertical = vertical + \
               min(bee_velocity_y, elevation - vertical - playerHeight)

    # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

    # Add a new pipe when the first is
    # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
    # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipe'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipe'][0],
                    (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipe'][1],
                    (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['floor_level'], (ground, elevation))
        window.blit(game_images['bee'], (horizontal, vertical))
        pygame.display.update()


def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if (vertical < pipeHeight + pipe['y'] and \
                abs(horizontal - pipe['x']) < game_images['pipe'][0].get_width()):
            return True

    for pipe in down_pipes:
        if (vertical + game_images['bee'].get_height() > pipe['y']) and \
                abs(horizontal - pipe['x']) < game_images['pipe'][0].get_width():
            return True
    return False


def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipe'][0].get_height()
    y2 = offset + \
         random.randrange(
             0, int(window_height - game_images['floor_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},

        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Buzy Bee Game')
    game_images['floor_level'] = pygame.image.load(floor).convert_alpha()
    game_images['bee'] = pygame.image.load(buzy_bee).convert_alpha()
    game_images['background'] = pygame.image.load(background).convert_alpha()
    game_images['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe_image)
                                                        .convert_alpha(),
                                                        180),
                                pygame.image.load(pipe_image).convert_alpha())
    print("WELCOME TO THE BUZY BEE GAME")
    print("Press space or enter to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int(
            (window_height - game_images['bee'].get_height()) / 2)
        ground = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or
                                                event.key == K_UP):
                    beegame()
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['bee'],
                                (horizontal, vertical))
                    window.blit(game_images['floor_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(FPS)
