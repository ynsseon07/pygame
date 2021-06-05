import os
import pygame
#####################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640  # 가로 크기
screen_height = 480  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Python Pang Game")  # 게임 이름

# FPS
clock = pygame.time.Clock()
#####################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
char = pygame.image.load(os.path.join(image_path, "character.png"))
char_size = char.get_rect().size
char_width = char_size[0]
char_height = char_size[1]
char_x_pos = (screen_width - char_width ) / 2
char_y_pos = screen_height - char_height - stage_height

# 캐릭터 이동 방향 & 속도
char_to_x = 0
char_speed = 5

# 무기 만들기 (위로 쏘는 무기)
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10


running = True 
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                char_to_x -= char_speed
            elif event.key == pygame.K_RIGHT:
                char_to_x += char_speed
            elif event.key == pygame.K_SPACE:   # 무기 발사
                weapon_x_pos = char_x_pos + (char_width / 2) - (weapon_width / 2)
                weapon_y_pos = char_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                char_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    char_x_pos += char_to_x

    if char_x_pos < 0:
        char_x_pos = 0
    elif char_x_pos > screen_width - char_width:
        char_x_pos = screen_width - char_width
    
    # 무기 위치 조정
    # 100, 200 -> x좌표는 그대로, y좌표는 180, 160, 140, ...
    weapons = [ [w[0], w[1] - weapon_speed ] for w in weapons] # 무기 위치를 위로
    
    # 천장에 닿은 무기 없애기 => 천장에 닿지 않은 무기들만 리스트로 저장
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 4. 충돌 처리
    
    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(char, (char_x_pos, char_y_pos))

    pygame.display.update()

pygame.quit()
