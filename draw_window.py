import pygame
import random

# 초기화
pygame.init()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris Complete Example")

# 게임 영역 설정
play_width = 300  # 10칸 (30px * 10)
play_height = 600  # 20칸 (30px * 20)
block_size = 30
top_left_x = (screen_width - play_width) // 2 - 50  # 왼쪽으로 조정
top_left_y = screen_height - play_height - 50


# 블록 클래스
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


# 격자선 그리기 함수
def draw_grid(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, (50, 50, 50),  # 어두운 회색
                         (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
    for j in range(len(grid[0]) + 1):
        pygame.draw.line(surface, (50, 50, 50),
                         (top_left_x + j * block_size, top_left_y),
                         (top_left_x + j * block_size, top_left_y + play_height))


# 다음 블록 표시 함수
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('britannic', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    # 블록 그리기
    for i, line in enumerate(shape.shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size,
                                  block_size, block_size), 0)
                # 테두리 추가
                pygame.draw.rect(surface, WHITE,
                                 (sx + j * block_size, sy + i * block_size,
                                  block_size, block_size), 1)

    surface.blit(label, (sx + 10, sy - 40))


# 메인 화면 그리기 함수
def draw_window(surface, grid, score=0, next_piece=None):
    # 1. 화면 초기화
    surface.fill(BLACK)

    # 2. 게임 제목
    font = pygame.font.SysFont('britannic', 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 15))

    # 3. 현재 점수
    font = pygame.font.SysFont('britannic', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # 4. 게임판 블록들 그리기
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != BLACK:  # 빈 칸이 아닌 경우만 그림
                pygame.draw.rect(surface, grid[i][j],
                                 (top_left_x + j * block_size,
                                  top_left_y + i * block_size,
                                  block_size, block_size), 0)
                pygame.draw.rect(surface, WHITE,
                                 (top_left_x + j * block_size,
                                  top_left_y + i * block_size,
                                  block_size, block_size), 1)  # 테두리

    # 5. 게임판 테두리
    pygame.draw.rect(surface, (150, 150, 150),
                     (top_left_x, top_left_y, play_width, play_height), 4)

    # 6. 격자선
    draw_grid(surface, grid)

    # 7. 다음 블록 표시
    if next_piece:
        draw_next_shape(next_piece, surface)


# 샘플 게임판 생성
def create_grid():
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    # 아래쪽에 일부 블록 생성 (테스트용)
    for i in range(15, 20):
        for j in range(10):
            if random.random() > 0.7:
                grid[i][j] = random.choice([RED, BLUE, GREEN, YELLOW])
    return grid


# 게임 루프
running = True
clock = pygame.time.Clock()
score = 0
next_piece = Piece()  # 다음 블록 생성

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                next_piece = Piece()  # Space로 다음 블록 변경 (테스트용)
                score += 100  # 점수 증가 (테스트용)

    # 샘플 게임판 생성
    grid = create_grid()

    # 전체 화면 그리기
    draw_window(screen, grid, score, next_piece)

    # 화면 업데이트
    pygame.display.update()
    clock.tick(30)

pygame.quit()
