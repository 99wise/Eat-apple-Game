﻿import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *
import random
import datetime
import sqlite3

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

def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Apple Licker")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()

player_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

# larva_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()

for k in range(1,3):
    potion = MySprite()
    potion.load("potion2.png",32,32,1)
    potion.positioin = random.randint(0,780),random.randint(0,580)
    potion_group.add(potion)
    
potion_group.draw(screen)


#게이머 마법사 그룹 초기화
player = MySprite()
player.load("farmer walk.png", 96, 96, 8)
player.position = 80, 80
player.direction = 4
player_group.add(player)

zombie = MySprite()
zombie.load("zombie walk.png", 96, 96, 8)
zombie.position = random.randint(0,780),random.randint(0,580)
player.direction = 4
zombie_group.add(zombie)

#초기화 음식요정그룹

for n in range(1,50):
    food = MySprite()
    food.load("food_low.png", 35, 35, 1)
    food.position = random.randint(0,780),random.randint(0,580)
    food_group.add(food)

game_over = False
player_moving = False
player_health = 0
zombie_moving = False
player_health = 0.1
zombie_moving = False

while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()     
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    elif keys[K_UP]:
        player.direction = 0
        player_moving = True
    elif keys[K_RIGHT]:
        player.direction = 2
        player_moving = True
    elif keys[K_DOWN]:
        player.direction = 4
        player_moving = True
    elif keys[K_LEFT]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False

    if keys[K_ESCAPE]: sys.exit()
    elif keys[K_w]:
        zombie.direction = 0
        zombie_moving = True
    elif keys[K_d]:
        zombie.direction = 2
        zombie_moving = True
    elif keys[K_s]:
        zombie.direction = 4
        zombie_moving = True
    elif keys[K_a]:
        zombie.direction = 6
        zombie_moving = True
    else:
        zombie_moving = False


    if not game_over:
        #캐릭터의 다양한 방향에 따라, 각기 다른 애니메이션 프레임워크를 사용한다.
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1

        zombie.first_frame = zombie.direction * zombie.columns
        zombie.last_frame = zombie.first_frame + zombie.columns-1

        if player.frame < player.first_frame:
            player.frame = player.first_frame
        
        if zombie.frame < zombie.first_frame:
            zombie.frame = zombie.first_frame

        if not player_moving:
            #버튼(인물이 이동하는 것을 멈출 때)을 멈추고 애니메이션 프레임 업데이트를 중단합니다
            player.frame = player.first_frame = player.last_frame
        else: 
            player.velocity = calc_velocity(player.direction, 2)
            player.velocity.x *= 10
            player.velocity.y *= 10

            
        if not zombie_moving:
            #버튼(인물이 이동하는 것을 멈출 때)을 멈추고 애니메이션 프레임 업데이트를 중단합니다
            zombie.frame = zombie.first_frame = zombie.last_frame
        else: 
            zombie.velocity = calc_velocity(zombie.direction, 2)
            zombie.velocity.x *= 2
            zombie.velocity.y *= 2

            
        if not zombie_moving:
            #버튼(인물이 이동하는 것을 멈출 때)을 멈추고 애니메이션 프레임 업데이트를 중단합니다
            zombie.frame = zombie.first_frame = zombie.last_frame
        else: 
            zombie.velocity = calc_velocity(zombie.direction, 2)
            zombie.velocity.x *= 2
            zombie.velocity.y *= 2

        #게이머 마법사 그룹 업데이트
        player_group.update(ticks, 50)
        zombie_group.update(ticks, 50)

        #모바일 플레이어
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > 700: player.X = 700
            if player.Y < 0: player.Y = 0
            elif player.Y > 500: player.Y = 500

        if zombie_moving:
            zombie.X += zombie.velocity.x
            zombie.Y += zombie.velocity.y
            if zombie.X < 0: zombie.X = 0
            elif zombie.X > 700: zombie.X = 700
            if zombie.Y < 0: zombie.Y = 0
            elif zombie.Y > 500: zombie.Y = 500

        attacker = None
        attacker = pygame.sprite.spritecollideany(player, food_group)
        huzom = None
        huzom = pygame.sprite.spritecollideany(player, zombie_group)

        if attacker != None:
            if pygame.sprite.collide_circle_ratio(0.65)(player,attacker):
                player_health +=2
                food_group.remove(attacker)

        if huzom != None:
            if pygame.sprite.collide_circle_ratio(0.25)(player,huzom):
                player_health -= 5
        if player_health > 100: player_health = 100

        #푸드 요정 팀 업데이트
        food_group.update(ticks, 50)


        if len(food_group) == 0:
            game_over = True
        if player_health == 0:
            game_over = True


    #텔레비전 화면을 깨끗이 하다
    screen.fill((50,50,100))

    #요정을 그리다
    food_group.draw(screen)
    player_group.draw(screen)
    zombie_group.draw(screen)

    #플레이어 혈행 그리기
    pygame.draw.rect(screen, (50,150,50,180), Rect(300,570,player_health*2,25))
    pygame.draw.rect(screen, (100,200,100,180), Rect(300,570,200,25), 2)

    

    if game_over:
        print_text(font, 300, 100, "G A M E   O V E R")
        end = time.time()
        et = end -start
        et = format(et,".2f")
        print_text(font, 300, 0, "시간: {0}초".format(et))
    pygame.display.update()
    
