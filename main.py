import pygame
import random
import math
pygame.init()

# Further development when done with base game
# Ai with neural network to learn how to play pong

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDLEHEIGHT, PADDLEWIDTH, PADDLEGAP = 100, 20, 30
BALLRADIUS = 8

TEXT_FONT = pygame.font.SysFont("comicsans", 45)


class Paddle:
    COLOR = WHITE
    VELOCITY = 10
    POINTS = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

class Ball:
    COLOR = WHITE
    X_VELOCITY = 10
    Y_VELOCITY = 10
    def __init__(self, x, y, radius):
        self.x = self.origin_x = x
        self.y = self.origin_y = y
        self.radius = radius
        self.max_velocity = 10

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
        if self.X_VELOCITY < 0:
            self.X_VELOCITY = self.max_velocity/2
        else:
            self.X_VELOCITY = -1*self.max_velocity/2
        self.Y_VELOCITY = 0


def main():
    running = True
    pause = False
    clock = pygame.time.Clock()

    left_paddle = Paddle(PADDLEGAP, HEIGHT // 2 - PADDLEHEIGHT//2, PADDLEWIDTH, PADDLEHEIGHT)
    right_paddle = Paddle(WIDTH - (PADDLEGAP + PADDLEWIDTH), HEIGHT // 2 - PADDLEHEIGHT//2, PADDLEWIDTH, PADDLEHEIGHT)
    # todo Paddle in the middle which moves up and down slowly that you can bounce off of, no special bounce though

    ball = Ball(WIDTH//2 - BALLRADIUS//2, HEIGHT//2 - BALLRADIUS//2, BALLRADIUS)

    pause_text = TEXT_FONT.render("Press Space to Unpause", 1, (0, 255, 0))

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause ^= True  # XOR toggle
        if not pause:
            draw(WIN, [left_paddle, right_paddle], ball, pause)
            keys = pygame.key.get_pressed()
            paddle_movement(keys, left_paddle, right_paddle)
            ball_movement(ball, left_paddle, right_paddle)
        else:
            WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT//2 - pause_text.get_height()//2))
            pygame.display.update()


def paddle_movement(keys, left_paddle, right_paddle):
    # Player 1 movements with W and S key, and bounds check
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + PADDLEHEIGHT + left_paddle.VELOCITY <= HEIGHT:
        left_paddle.move(up=False)

    # Player 2 movements with up and down key, and bounds check
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + PADDLEHEIGHT + right_paddle.VELOCITY <= HEIGHT:
        right_paddle.move(up=False)


def ball_movement(ball, left_paddle, right_paddle):
    ball.x += ball.X_VELOCITY
    ball.y += ball.Y_VELOCITY
    ball_radius = ball.radius
    ball_y = ball.y
    ball_x = ball.x
    left_paddle_y = left_paddle.y
    right_paddle_y = right_paddle.y
    left_paddle_x = left_paddle.x
    right_paddle_x = right_paddle.x

    # Left paddle
    if left_paddle_x <= ball_x <= left_paddle_x+PADDLEWIDTH:
        # Collision with left paddle
        if left_paddle_y-ball_radius < ball_y < left_paddle_y + PADDLEHEIGHT+ball_radius:
            ball_displacement = left_paddle_y + PADDLEHEIGHT // 2 - ball_y
            if ball_displacement < -3:  # Top
                ball.Y_VELOCITY = -1*ball_displacement / ((left_paddle.height / 2) / ball.max_velocity)
            elif ball_displacement > 3:  # Bottom
                ball.Y_VELOCITY = -1*ball_displacement / ((left_paddle.height / 2) / ball.max_velocity)
            elif -3 <= ball_displacement <= 3:  # Middle
                ball.Y_VELOCITY = 0
                ball.X_VELOCITY = -ball.max_velocity
            ball.X_VELOCITY = ball.max_velocity
        elif ball_y + ball_radius == left_paddle_y:
            ball.Y_VELOCITY = -ball.max_velocity
        elif ball_y - ball_radius == left_paddle_y + PADDLEHEIGHT:
            ball.Y_VELOCITY = ball.max_velocity
    elif ball_x < 0:
        right_paddle.POINTS += 1
        ball.reset()
    # Right paddle
    if right_paddle_x + PADDLEWIDTH >= ball_x >= right_paddle_x:
        # Collision with right paddle
        if right_paddle_y - ball_radius < ball_y < right_paddle_y + PADDLEHEIGHT + ball_radius:
            ball_displacement = right_paddle.y + PADDLEHEIGHT//2 - ball.y
            if ball_displacement < -ball_radius:  # Top
                ball.Y_VELOCITY = -1*ball_displacement / ((right_paddle.height / 2) / ball.max_velocity)
            elif ball_displacement > ball_radius:  # Bottom
                ball.Y_VELOCITY = -1*ball_displacement / ((right_paddle.height / 2) / ball.max_velocity)
            elif -ball_radius <= ball_displacement <= ball_radius:  # Middle
                ball.Y_VELOCITY = 0
                ball.X_VELOCITY = ball.max_velocity
            ball.X_VELOCITY = -ball.max_velocity
        elif ball_y + ball_radius == right_paddle_y:
            ball.Y_VELOCITY = -ball.max_velocity
        elif ball_y - ball_radius == right_paddle_y + PADDLEHEIGHT:
            ball.Y_VELOCITY = ball.max_velocity
            #ball.X_VELOCITY *= -1
    elif ball_x > WIDTH:
        left_paddle.POINTS += 1
        ball.reset()

    if not 0 <= ball_y <= HEIGHT:  # Collision with bottom and top
        ball.y -= ball.Y_VELOCITY
        ball.Y_VELOCITY *= -1


def draw(win, paddles, ball, pause):
    win.fill(BLACK)
    # Draw Paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw points
    left_points = TEXT_FONT.render(f"{paddles[0].POINTS}", 1, WHITE)
    right_points = TEXT_FONT.render(f"{paddles[1].POINTS}", 1, WHITE)
    win.blit(left_points, (WIDTH//4 - left_points.get_width()//2, 20))
    win.blit(right_points, (3*WIDTH // 4 - right_points.get_width() // 2, 20))

    # Draw dotted line in the middle
    dotted_width = PADDLEWIDTH//2
    dotted_height = PADDLEHEIGHT//2
    dotted_gap = 20
    start_y = 0
    center_x = (WIDTH//2) - (dotted_width//2)
    while start_y < HEIGHT:
        pygame.draw.rect(win, WHITE, (center_x, start_y, dotted_width, dotted_height))
        start_y += dotted_height + dotted_gap
    ball.draw(win)
    pygame.display.update()


if __name__ == '__main__':
    main()
