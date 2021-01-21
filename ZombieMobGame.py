import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *
import random
import datetime
import sqlite3

conn = sqlite3.connect('./final/game.db', isolation_level=None)
c = conn.cursor()

#테이블 생성
c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, rectime text, regdate text)")

def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #위
        velocity.y = -vel
    elif direction == 2: #오른쪽
        velocity.x = vel
    elif direction == 4: #아래
        velocity.y = vel
    elif direction == 6: #왼쪽
        velocity.x = -vel
    return velocity

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Apple Licker")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()

#요정 팀 만들기
player_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

#게이머 마법사 그룹 초기화
player = MySprite()
player.load("farmer walk.png", 96, 96, 8)
player.position = 80, 80
player.direction = 4
player_group.add(player)

#초기화 음식요정그룹

for n in range(1,50):
    food = MySprite()
    food.load("food_low.png", 35, 35, 1)
    food.position = random.randint(0,780),random.randint(0,580)
    food_group.add(food)

game_over = False
player_moving = False
player_health = 0

#걸린 시간, 날짜 


while True:
    id = input("Ready? Input Your name>> ")             
    user = GameUser(id)                     
    user.user_info()

    start = time.time()
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    elif keys[K_UP] or keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False


    if not game_over:
        #캐릭터의 다양한 방향에 따라, 각기 다른 애니메이션 프레임워크를 사용한다.
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1
        if player.frame < player.first_frame:
            player.frame = player.first_frame

        if not player_moving:
            #버튼(인물이 이동하는 것을 멈출 때)을 멈추고 애니메이션 프레임 업데이트를 중단합니다
            player.frame = player.first_frame = player.last_frame
        else: 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 1.5
            player.velocity.y *= 1.5

        #게이머 마법사 그룹 업데이트
        player_group.update(ticks, 50)

        #모바일 플레이어
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > 700: player.X = 700
            if player.Y < 0: player.Y = 0
            elif player.Y > 500: player.Y = 500

        #플레이어가 음식과 충돌하는지, 열매를 먹는지 검사합니다.
        attacker = None
        attacker = pygame.sprite.spritecollideany(player, food_group)
        if attacker != None:
            if pygame.sprite.collide_circle_ratio(0.65)(player,attacker):
                player_health +=2
                food_group.remove(attacker)
        if player_health > 100: player_health = 100
        #푸드 요정 팀 업데이트
        food_group.update(ticks, 50)

        if len(food_group) == 0:
            game_over = True
    #텔레비전 화면을 깨끗이 하다
    screen.fill((50,50,100))

    #요정을 그리다
    food_group.draw(screen)
    player_group.draw(screen)

    #플레이어 혈행 그리기
    pygame.draw.rect(screen, (50,150,50,180), Rect(300,570,player_health*2,25))
    pygame.draw.rect(screen, (100,200,100,180), Rect(300,570,200,25), 2)

    if game_over:
        print_text(font, 300, 100, "G A M E   O V E R")
        end = time.time()
        et = end -start
        et = format(et,"2f")
        print_text(font, 300, -300, "시간: {0}초".format(et))

        c.execute("INSERT INTO users (id, rectime, regdate) VALUES(?,?,?,?,?,?)",(id, et, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        c.close()
    
    pygame.display.update()
    

