import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
#pygame.mixer.music.load('tetris.mp3')

#Global variables
screen_size = pygame.display.get_desktop_sizes()[0]
s_width = screen_size[0]
s_height = screen_size[1]
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = (s_height - play_height) // 3

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("britannic", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

# 게임 시작 여부를 판단하는 변수 추가
# 이 변수가 True가 되면 게임이 시작됩니다.
game_started = False

win = pygame.display.set_mode((s_width, s_height))

while True:
    # 화면을 매번 검은색으로 지워줍니다.
    win.fill((0, 0, 0))

    # Pygame 이벤트(마우스 클릭, 키보드 입력 등)를 처리하는 부분
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        # 만약 키보드의 어떤 키라도 눌렸다면
        if event.type == pygame.KEYDOWN:
            # game_started 변수를 True로 바꿔줍니다.
            game_started = True

    # game_started가 False일 때만 (아직 키를 누르지 않았을 때)
    # 시작 문구를 화면에 그립니다.
    if game_started == False:
        draw_text_middle(win, 'Press Any Key To Start', 60, (255, 255, 255))

    # 화면에 그린 내용을 실제로 보여줍니다.
    pygame.display.update()
