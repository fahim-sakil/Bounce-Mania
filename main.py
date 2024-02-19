import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 500

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bounce Mania')

# define font
font = pygame.font.SysFont('calibri', 30)

# define game variables
margin = 50
cpu_score = 0
player_score = 0
live_ball = False
winner = 0
speed_increase = 0



# define colours
bg_black = (0, 0, 0)
white = (255, 255, 255)


def draw_board():
    screen.fill(bg_black)
    pygame.draw.line(screen, white, (0, margin), (screen_width, margin), 2)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(x, y, 20, 100)
        self.speed = 5
        self.ai_speed = 5

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > (margin+5):
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height-5:
            self.rect.move_ip(0, self.speed)

    def draw(self):
        pygame.draw.rect(screen, (50, 150, 255), self.rect)

    def ai(self):
        # ai to move the paddle automatically
        # move down
        if self.rect.centery < bounce.rect.top and self.rect.bottom < screen_height-5:
            self.rect.move_ip(0, self.ai_speed)
        # move up
        if self.rect.centery > bounce.rect.bottom and self.rect.top > margin+5:
            self.rect.move_ip(0, -1 * self.ai_speed)


class ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):

        # check collision with top margin
        if self.rect.top < margin:
            self.speed_y *= -1
        # check collision with bottom of the screen
        if self.rect.bottom > screen_height:
            self.speed_y *= -1
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1

        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.left > screen_width:
            self.winner = -1

        # update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(screen, (255, 165, 0), (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0  # 1 is the player and -1 is the CPU


# create paddles
player_paddle = paddle(screen_width - 40, screen_height // 2)
cpu_paddle = paddle(20, screen_height // 2)

# create bounce ball
bounce = ball(screen_width - 60, screen_height // 2 + 50)


fps = 60

# create game loop
run = True
while run:
    fpsClock.tick(fps)

    draw_board()
    draw_text('COMPUTER: ' + str(cpu_score), font, white, 20, 15)
    draw_text('YOU: ' + str(player_score), font, white, screen_width - 100, 15)
    draw_text('LEVEL: ' + str(abs(bounce.speed_x)-3), font, white, screen_width // 2 - 20, 15)

    # draw paddles
    player_paddle.draw()
    cpu_paddle.draw()



    if live_ball == True:
        speed_increase += 1
        winner = bounce.move()
        if winner == 0:
            # draw ball
            bounce.draw()
            # move paddles
            player_paddle.move()
            cpu_paddle.ai()
        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                cpu_score += 1

    # print player instructions
    if live_ball == False:
        if winner == 0:
            draw_text('PRESS SPACE OR', font, white, 200, screen_height // 2 - 100)
            draw_text('CLICK ANYWHERE TO START', font, white, 140, screen_height // 2-50)
        if winner == 1:
            draw_text('YOU WON!', font, (0, 255, 0), 220, screen_height // 2 - 170)
            draw_text('PRESS SPACE OR', font, white, 200, screen_height // 2 - 100)
            draw_text('CLICK ANYWHERE TO RESTART', font, white, 140, screen_height // 2 - 50)
        if winner == -1:
            draw_text('COMPUTER WON!', font, (255, 0, 0), 190, screen_height // 2 - 170)
            draw_text('PRESS SPACE OR', font, white, 200, screen_height // 2 - 100)
            draw_text('CLICK ANYWHERE TO RESTART', font, white, 140, screen_height // 2 - 50)

    key1 = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN or key1[pygame.K_SPACE]) and live_ball == False:
            live_ball = True
            bounce.reset(screen_width - 60, screen_height // 2 + 50)

    if speed_increase > 800:
        speed_increase = 0
        if bounce.speed_x < 0:
            bounce.speed_x -= 1
        if bounce.speed_x > 0:
            bounce.speed_x += 1
        if bounce.speed_y < 0:
            bounce.speed_y -= 1
        if bounce.speed_y > 0:
            bounce.speed_y += 1

    pygame.display.update()

pygame.quit()