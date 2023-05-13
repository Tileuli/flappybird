import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_Y = SCREEN_HEIGHT * 0.8
game_images = {}
game_sounds = {}
player = 'sprites/yellowbird-midflap.png'
background = 'sprites/background-day.png'
pipe = 'sprites/pipe-green.png'

def welcomeSCREEN():
    player_x = int(SCREEN_WIDTH / 8)
    player_y = int((SCREEN_HEIGHT - game_images['player'].get_height()) / 2)
    message_x = int((SCREEN_WIDTH - game_images['message'].get_width()) / 2)
    message_y = int(SCREEN_HEIGHT * 0.2)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(game_images['background'], (0, 0))
                SCREEN.blit(game_images['message'], (message_x, message_y))
                SCREEN.blit(game_images['player'], (player_x, player_y))
                SCREEN.blit(game_images['base'], (base_x, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)

def mainGame():
    score = 0
    high_score = 0
    player_x = int(SCREEN_WIDTH / 5)
    player_y = int(SCREEN_HEIGHT / 2)
    base_x = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREEN_WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREEN_WIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerAccY = 1

    playerFlapVel = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    playerVelY = playerFlapVel
                    playerFlapped = True
                    game_sounds['wing'].play()

        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = player_x + game_images['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                game_sounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
            playerHeight = game_images['player'].get_height()
            player_y = player_y + min(playerVelY, GROUND_Y - player_y - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            SCREEN.blit(game_images['base'], (base_x, GROUND_Y))
            SCREEN.blit(game_images['player'], (player_x, player_y))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (SCREEN_WIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(game_images['numbers'][digit], (Xoffset, SCREEN_HEIGHT * 0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y > GROUND_Y - 25 or player_y < 0:
        game_sounds['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if (player_y < pipeHeight + pipe['y']) and (
                abs(player_x - pipe['x']) < game_images['pipe'][0].get_width() - 15):
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (player_y + game_images['player'].get_height() > pipe['y']) and (
                abs(player_x - pipe['x']) < game_images['pipe'][0].get_width() - 15):
            game_sounds['hit'].play()
            return True

    return False

def getRandomPipe():
    pipeHeight = game_images['pipe'][0].get_height()
    offset = SCREEN_HEIGHT / 4
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - game_images['base'].get_height() - 1.2 * offset))
    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    game_images['numbers'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha()
    )
    game_images['message'] = pygame.image.load('sprites/message.png').convert_alpha()
    game_images['base'] = pygame.image.load('sprites/base.png').convert_alpha()
    game_images['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )
    game_images['background'] = pygame.image.load(background).convert_alpha()
    game_images['player'] = pygame.image.load(player).convert_alpha()

    # Game Sounds
    game_sounds['die'] = pygame.mixer.Sound('sprites/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('sprites/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('sprites/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('sprites/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('sprites/wing.wav')

    while True:
        welcomeSCREEN()
        mainGame()
