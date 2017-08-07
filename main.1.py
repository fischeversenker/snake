from sys import exit
from random import randint
import pygame
from pygame.locals import *
from pygame.math import Vector2

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE    = 20
FPS           = 8

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.running = False
        self.area = Vector2(SCREEN_WIDTH / BLOCK_SIZE, SCREEN_HEIGHT / BLOCK_SIZE)
        self.player = Snake(self.area)
        self.foods = []
        self.background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.background.fill(Color(0, 0, 0, 255))

    def gameloop(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.placeFood(Vector2(tuple(map(lambda x: int(x / BLOCK_SIZE), pygame.mouse.get_pos()))))
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    self.player.setDirection((-1, 0))
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    self.player.setDirection((0, 1))
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    self.player.setDirection((1, 0))
                elif event.type == KEYDOWN and event.key == K_UP:
                    self.player.setDirection((0, -1))

            self.screen.blit(self.background, (0, 0))
            self.player.update()

            #### FOODS
            if len(self.foods) == 0:
                self.placeFood(Helper.randomPos(self.area))
            for i, food in enumerate(self.foods):
                if self.player.pos.x == food.pos.x and self.player.pos.y == food.pos.y:
                    self.player.eat(food)
                    del self.foods[i]
                else:
                    Renderer.drawCircle(self.screen, food)

            Renderer.drawSnake(self.screen, self.player)

            pygame.display.update()
            clock.tick(FPS)

    def start(self):
        self.running = True
        self.gameloop()
    
    def placeFood(self, pos):
        self.foods.append(Food(pos, Helper.randomColor()))
        

class Snake():
    def __init__(self, area, pos=Vector2(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.area = area
        self.pos = pos
        self.color = Color(255, 255, 255, 255)
        self.tail = []
        self.ate = False
        self.direction = Vector2(1, 0)
        self.beep = pygame.mixer.Sound("beep.wav")

    def update(self):
        (dirX, dirY) = self.direction

        if self.ate:
            self.tail = [Vector2(self.pos)] + self.tail
            self.ate = False

        if len(self.tail) > 0:
            self.tail = [Vector2(self.pos)] + self.tail
            del self.tail[-1]

        self.pos.x += dirX
        self.pos.y += dirY
        if self.pos.x < 0:
            self.pos.x = self.area.x - 1
        if self.pos.y < 0:
            self.pos.y = self.area.y - 1
        if self.pos.x + 1 > self.area.x:
            self.pos.x = 0
        if self.pos.y + 1 > self.area.y:
            self.pos.y = 0

        for block in self.tail:
            if block == self.pos:
                pygame.time.wait(4000)

    def setDirection(self, dir):
        (dirX, dirY) = self.direction
        (newX, newY) = dir
        if dirX + newX != 0 and dirY + newY != 0:
            self.direction = dir

    def eat(self, food):
        self.ate = True
        self.playSound()

    def playSound(self):
        pan = self.pos.x / self.area.x
        channel = self.beep.play()
        channel.set_volume(1.0-pan, pan) 

class Food():
    def __init__(self, pos, color):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.color = color
        self.age = 0

class Helper():
    @staticmethod
    def randomPos(area):
        randX = randint(0, area.x - 1)
        randY = randint(0, area.y - 1)
        return Vector2(randX, randY)
    
    @staticmethod
    def randomColor():
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return Color(r, g, b, 255)

class Renderer():
    @staticmethod
    def drawSnake(screen, snake):
        rect = Rect(snake.pos.x * BLOCK_SIZE, snake.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, snake.color, rect)
        for bodyPart in snake.tail:
            rect = Rect(bodyPart.x * BLOCK_SIZE, bodyPart.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, snake.color, rect)

    @staticmethod
    def drawCircle(screen, sprite):
        rect = Rect(sprite.pos.x * BLOCK_SIZE, sprite.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.ellipse(screen, sprite.color, rect)

game = Game()
game.start()
