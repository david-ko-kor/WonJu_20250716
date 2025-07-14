import pygame
import random

# 초기화
pygame.init()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)


# 블록 클래스 (수정된 버전)
class Piece:
    shapes = [
        ["1111"],  # I
        ["11", "11"],  # O
        ["111", "010"],  # T
        ["111", "100"],  # L
        ["111", "001"],  # J
        ["011", "110"],  # S
        ["110", "011"]  # Z
    ]
    colors = [CYAN, YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED]

    def __init__(self):
        self.shape_idx = random.randint(0, len(self.shapes) - 1)
        self.shape = self.shapes[self.shape_idx]
        self.color = self.colors[self.shape_idx]
        self.rotation = 0
        self.x = 0
        self.y = 0


# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Next Shape Preview Example")

# 게임 영역 설정
play_width = 300
play_height = 600
block_size = 30
top_left_x = (screen_width - play_width) // 2 - 200
top_left_y = (screen_height - play_height) // 2


# 다음 블록 표시 함수 (수정된 버전)
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('britannic', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':  # 문자열 '1'로 비교
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size,
                                  block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 40))


# 게임 루프
running = True
clock = pygame.time.Clock()
next_piece = Piece()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                next_piece = Piece()

    screen.fill(BLACK)
    draw_next_shape(next_piece, screen)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
