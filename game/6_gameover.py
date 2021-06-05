# 1. 모든 공을 없애면 게임 종료 (성공)
# 2. 캐릭터는 공에 닿으면 게임 종료 (실패)
# 3. 시간 제한 99초 초과시 게임 종료 (실패)


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
char_to_x_left = 0
char_to_x_right = 0
char_speed = 5

# 무기 만들기 (위로 쏘는 무기)
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "Balloon1.png")),
    pygame.image.load(os.path.join(image_path, "Balloon2.png")),
    pygame.image.load(os.path.join(image_path, "Balloon3.png")),
    pygame.image.load(os.path.join(image_path, "Balloon4.png")),
]

# 공 크기에 따른 최초 스피드 => 공이 튕겨 올라가는 거므로 음수(마이너스)
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 에 해당하는 값

# 공들
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50,  # 공의 x좌표
    "pos_y" : 50,  # 공의 y좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3,    # 공의 x축 이동방향, -3이면 왼쪽으로 3이면 오른쪽으로
    "to_y" : -6,   # 공의 y축 이동방향
    "init_spd_y" : ball_speed_y[0] # y 최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)

# 시간 정보
total_time = 100
start_time = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메시지
# Time Over(시간초과)
# Mission Complete (성공)
# Game Over(캐릭터가 공에 맞음)
game_result = "Game Over"


running = True 
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                char_to_x_left -= char_speed
            elif event.key == pygame.K_RIGHT:
                char_to_x_right += char_speed
            elif event.key == pygame.K_SPACE:   # 무기 발사
                weapon_x_pos = char_x_pos + (char_width / 2) - (weapon_width / 2)
                weapon_y_pos = char_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                char_to_x_left = 0
            elif event.key == pygame.K_RIGHT:
                char_to_x_right = 0

    # 3. 게임 캐릭터 위치 정의
    char_x_pos += char_to_x_left + char_to_x_right

    if char_x_pos < 0:
        char_x_pos = 0
    elif char_x_pos > screen_width - char_width:
        char_x_pos = screen_width - char_width
    
    # 무기 위치 조정 => 리스트 weapons의 각 원소는 무기의 x,y좌표를 가짐
    # 100, 200 -> x좌표는 그대로, y좌표는 180, 160, 140, ...
    weapons = [ [w[0], w[1] - weapon_speed ] for w in weapons] # 무기 위치를 위로
    
    # 천장에 닿은 무기 없애기 => 천장에 닿지 않은 무기들만 리스트로 저장
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 공이 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 공의 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        # if문은 공이 스테이지에 처음 튕겼을때 / else는 처음 튕기고 그 이후부터의 속도
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리
    
    # 캐릭터 rect 정보 업데이트
    char_rect = char.get_rect()
    char_rect.left = char_x_pos
    char_rect.top = char_y_pos

    # 각 공에 대한 처리
    for ball_idx, ball_val in enumerate(balls): # 바깥조건
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 체크
        if char_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons): # 안쪽조건
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠줌
                if ball_img_idx < 3:
                    # 현재 공 크기 정보 가지고옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2,  # 공의 x좌표
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2,  # 공의 y좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : -3,    # 공의 x축 이동방향, -3이면 왼쪽으로 3이면 오른쪽으로
                        "to_y" : -6,   # 공의 y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2,  # 공의 x좌표
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2,  # 공의 y좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : 3,    # 공의 x축 이동방향, -3이면 왼쪽으로 3이면 오른쪽으로
                        "to_y" : -6,   # 공의 y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })

                break
        else: # 계속 게임을 진행
            continue # 안쪽 for문 조건 맞지 않으면 continue
        break # 안쪽 for문에서 break 만나면 여기로 진입 => 이중 for문 한번에 탈출

    # for 바깥조건:
    #     바깥동작
    #     for 안쪽조건:
    #         안쪽동작
    #         if 충돌하면:
    #             break
    #     else:
    #         continue
    #     break
    # ==> for와 else를 같이 적음 (일종의 트릭, break를 통해 이중 for문을 한번에 빠져나오기 위함)


    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False


    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(char, (char_x_pos, char_y_pos))

    # 경과 시간 계산
    running_time = (pygame.time.get_ticks() - start_time) / 1000
    remain_time = game_font.render("Time : {}".format(int(total_time - running_time)), True, (255, 255, 255))
    screen.blit(remain_time, (10, 10))

    # 시간 초과할 경우
    if total_time - running_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 0, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2초 대기
pygame.time.delay(2000)

pygame.quit()
