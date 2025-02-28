import pygame
import random
import time

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Pong')
        pygame.display.set_icon(pygame.image.load('./assets/img/logo.png'))

        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('assets/fonts/vcr.ttf', 36)
        self.youWinFont = pygame.font.Font('./assets/fonts/upheavtt.ttf', 72)

        self.leftPaddle = pygame.image.load('./assets/img/paddle.png')
        self.leftPaddle_pos = [10, (self.screen.height / 2) - (self.leftPaddle.height / 2)]
        self.leftPaddle_moving = 0

        self.rightPaddle = pygame.image.load('./assets/img/paddle.png')
        self.rightPaddle_pos = [self.screen.width - (10 + self.rightPaddle.width), (self.screen.height / 2) - (self.leftPaddle.height / 2)]
        self.rightPaddle_moving = 0

        self.separator = pygame.image.load('./assets/img/separator.png')
        self.separator_alpha = 255

        self.ball_size = [10, 10]
        self.ball_start_pos = [(self.screen.width / 2) - (self.ball_size[0] / 2), (self.screen.height / 2) - (self.ball_size[1] / 2)]
        self.ball_pos = self.ball_start_pos
        self.acceleration = [1,0]

        self.leftScore = 0
        self.rightScore = 0

    def run(self):
        self.running = True

        while self.running:
            self.screen.fill((0, 0, 0))

            self.ball_pos[0] += self.acceleration[0] * 3
            self.ball_pos[1] += self.acceleration[1] * 3
            
            self.ball = pygame.draw.ellipse(self.screen, (255,255,255), (self.ball_pos[0], self.ball_pos[1], self.ball_size[0], self.ball_size[1]))

            self.screen.blit(self.separator, (self.screen.width / 2 - 2.5, 0))

            self.separator.set_alpha(self.separator_alpha)

            self.leftPaddle_pos[1] += self.leftPaddle_moving
            self.rightPaddle_pos[1] += self.rightPaddle_moving

            self.screen.blit(self.leftPaddle, self.leftPaddle_pos)
            self.screen.blit(self.rightPaddle, self.rightPaddle_pos)

            self.leftScore_text = self.font.render(f"{self.leftScore}", False, (255,255,255))
            self.rightScore_text = self.font.render(f"{self.rightScore}", False, (255,255,255))

            self.leftScore_text_pos = ((pygame.display.get_window_size()[0] / 3) - self.leftScore_text.width, 25)
            self.rightScore_text_pos = ((pygame.display.get_window_size()[0] - pygame.display.get_window_size()[0] / 3) - self.rightScore_text.width / 2, 25)

            self.screen.blit(self.leftScore_text, self.leftScore_text_pos)
            self.screen.blit(self.rightScore_text, self.rightScore_text_pos)

            # self.collidingWithLeft = (self.leftPaddle_pos[0] < self.ball_pos[0] + self.ball_size[0] and 
            #                             self.leftPaddle_pos[0] + 5 > self.ball_pos[0] and 
            #                             self.leftPaddle_pos[1] < self.ball_pos[1] + self.ball_size[1] and 
            #                             self.leftPaddle_pos[1] + 480 > self.ball_pos[1])
            # self.collidingWithRight = (self.rightPaddle_pos[0] < self.ball_pos[0] + self.ball_size[0] and
            #                             self.rightPaddle_pos[0] + 5 > self.ball_pos[0] and
            #                             self.rightPaddle_pos[1] < self.ball_pos[1] + self.ball_size[1] and
            #                             self.rightPaddle_pos[1] + 480 > self.ball_pos[1])

            self.collidingWithLeft = (self.leftPaddle_pos[0] < self.ball_pos[0] + self.ball_size[0] and 
                                        self.leftPaddle_pos[0] + 5 > self.ball_pos[0] and 
                                        self.leftPaddle_pos[1] < self.ball_pos[1] + self.ball_size[1] and 
                                        self.leftPaddle_pos[1] + 50 > self.ball_pos[1])
            self.collidingWithRight = (self.rightPaddle_pos[0] < self.ball_pos[0] + self.ball_size[0] and
                                        self.rightPaddle_pos[0] + 5 > self.ball_pos[0] and
                                        self.rightPaddle_pos[1] < self.ball_pos[1] + self.ball_size[1] and
                                        self.rightPaddle_pos[1] + 50 > self.ball_pos[1])


            if self.collidingWithLeft:
                self.acceleration[0] *= -1
                self.acceleration[1] = (self.ball_pos[1] - (self.leftPaddle_pos[1] + 25)) / 25

            if self.collidingWithRight:
                self.acceleration[0] *= -1
                self.acceleration[1] = (self.ball_pos[1] - (self.rightPaddle_pos[1] + 25)) / 25

            if self.ball_pos[0] > 640:
                self.leftScore += 1
                self.reset()
            elif self.ball_pos[0] < 0:
                self.rightScore += 1
                self.reset()

            if self.ball_pos[1] > 480 or self.ball_pos[1] < 0:
                self.acceleration[1] *= -1

            if self.leftScore > 10:
                self.leftWins()
            if self.rightScore > 10:
                self.rightWins()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rightPaddle_moving = -3
                    if event.key == pygame.K_DOWN:
                        self.rightPaddle_moving = 3
                    if event.key == pygame.K_w:
                        self.leftPaddle_moving = -3
                    if event.key == pygame.K_s:
                        self.leftPaddle_moving = 3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.rightPaddle_moving = 0
                    if event.key == pygame.K_DOWN:
                        self.rightPaddle_moving = 0
                    if event.key == pygame.K_w:
                        self.leftPaddle_moving = 0
                    if event.key == pygame.K_s:
                        self.leftPaddle_moving = 0

            pygame.display.update()
            self.clock.tick(120)

    def reset(self):
        self.leftPaddle_pos = [10, (self.screen.height / 2) - (self.leftPaddle.height / 2)]  
        self.rightPaddle_pos = [self.screen.width - (10 + self.rightPaddle.width), (self.screen.height / 2) - (self.leftPaddle.height / 2)]
        self.ball_pos[0] = self.screen.width / 2 - self.ball_size[0] / 2
        self.ball_pos[1] = self.screen.height / 2 - self.ball_size[1] / 2
        self.acceleration = [1,0]

    def leftWins(self):
        self.running = False
        youWinText = self.youWinFont.render("Left Wins!", False, (255,255,255))

        while True:
            self.screen.blit(youWinText, (self.screen.width / 2 - youWinText.width / 2, self.screen.height / 2 - youWinText.height / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.K_ENTER:
                    self.reset()
                    self.run()
            
            pygame.display.update()
            self.clock.tick(1)
    
    def rightWins(self):
        self.running = False
        youWinText = self.youWinFont.render("Right Wins!", False, (255,255,255))

        while True:
            self.screen.blit(youWinText, (self.screen.width / 2 - youWinText.width / 2, self.screen.height / 2 - youWinText.height / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.K_ENTER:
                    self.reset()
                    self.run()
					
            
            pygame.display.update()
            self.clock.tick(1)

Game().run()
