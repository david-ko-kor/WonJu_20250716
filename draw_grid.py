import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

# 전역 변수 설정
screen_size = pygame.display.get_desktop_sizes()[0]
s_width = screen_size[0]
s_height = screen_size[1]
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = (s_height - play_height) // 3

# draw_grid 함수 정의 (제공해주신 코드)
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    # 가로선 그리기
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        
    # 세로선 그리기
    for j in range(len(grid[0])): # len(grid[0])으로 변경하면 더 정확합니다.
        pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


# 메인 루프에서 사용할 더미 게임판(grid) 생성
# 10칸 x 20칸 크기의 빈 격자를 만듭니다.
# 20은 세로 칸 수, 10은 가로 칸 수입니다.
dummy_grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

# 게임 창 생성
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Grid Example")

# 메인 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    # 화면을 검은색으로 채웁니다.
    win.fill((0, 0, 0))

    # dummy_grid를 인수로 전달하여 격자를 그립니다.
    draw_grid(win, dummy_grid)
    
    # 화면을 업데이트하여 격자를 보여줍니다.
    pygame.display.update()
