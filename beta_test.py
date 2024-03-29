import pygame
import os
import random
import time

pygame.init()
pygame.font.init()

score=0
health=3
width,height=900,500
root=pygame.display.set_mode((width,height))
run=True
FPS=pygame.time.Clock()
ship_width,ship_height=50,40
VEL=5
all_bullets=[]
text=pygame.font.SysFont('comicsans',40)
player_start_x,player_start_y=width/2-ship_width,450
enemy_lst=[]
enemy_speed=1

player1=pygame.image.load(r"PyGame 3\pics\spaceship_red.png")
player1=pygame.transform.scale(player1,(ship_width,ship_height))

enemy_pic=pygame.image.load(r"PyGame 3\pics\spaceship_yellow.png")
enemy_pic=pygame.transform.scale(enemy_pic,(ship_width,ship_height))
enemy_pic=pygame.transform.rotate(enemy_pic,180)

bg=pygame.transform.scale(pygame.image.load(r"PyGame 3\pics\space.png"),(width,height))


class Level:
    def __init__(self,level_id,enemy_count):
        self.level_id=level_id
        self.enemy_count=enemy_count

level1=Level(1,9)
level2=Level(2,19)
level3=Level(3,29)
lst=[level1,level2,level3]

def movement(keys,red):
    if keys[pygame.K_w] and red.y>0:
        red.y-=VEL
    if keys[pygame.K_s] and red.y+red.height+VEL<height:
        red.y+=VEL
    if keys[pygame.K_a] and red.x>0:
        red.x-=VEL
    if keys[pygame.K_d] and red.x+red.width+VEL<width:
        red.x+=VEL
    
def bullet_movement():
    global score,health
    for bullet in all_bullets:
        bullet.y-=5
        if bullet.y<=0:
            all_bullets.remove(bullet)


##COLLISION
# def bullet_movement(player2):
#     global score
#     for bullet in all_bullets:
#         bullet.y-=5
#         # print(len(all_bullets),bullet.y)
#         if player2.colliderect(bullet):
#             score-=10
#             print(score)
#             all_bullets.remove(bullet)

def get_enemy_coords():
    global num,current_level
    # if red.y>=player_start_y:
        # enemy_x=random.randint(0,width)
        # enemy_y=0
        # enemy=pygame.Rect(enemy_x,enemy_y,ship_width,ship_height)
        # enemy_lst.append([enemy_x,enemy_y])
        # # if len(enemy_lst)<10:
        # #     enemy_lst.append(enemy)
        # root.blit(enemy_pic,(enemy.x,enemy.y))
    enemy=pygame.Rect(random.randint(0,width-ship_width),random.randint(-500,-100),ship_width,ship_height)
    num=0
    current_level=lst[num]
    if len(enemy_lst)<=current_level.enemy_count:
        enemy_lst.append(enemy)
    # enemy_lst.append(enemy)



def draw_enemies():
    global score,health
    for i in enemy_lst:
        # pygame.draw.rect(bg,(255,255,255),i)
        i[1]+=enemy_speed
        root.blit(enemy_pic,(i[0],i[1]))
        for bullet in all_bullets:
            if i.colliderect(bullet):
                score+=10
                enemy_lst.remove(i)
                all_bullets.remove(bullet)
        
        if i[1]>=height:
            enemy_lst.remove(i)
            score-=10
            health-=1
        
        

def end_level():
    global score
    if score==100:
        passed_level=text.render(f"Level:{current_level.level_id} Passed",1,(255,255,255))
        root.blit(passed_level,(width//2-passed_level.get_width()//2,height//2-passed_level.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        score=0
        for i in enemy_lst:
            enemy_lst.remove(i)
    
    elif health==0:
        passed_level=text.render(f"YOU LOSE",1,(255,255,255))
        root.blit(passed_level,(width//2-passed_level.get_width()//2,height//2-passed_level.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        score=0
        for i in enemy_lst:
            enemy_lst.remove(i)


def main():
    global run,all_bullets,score
    red=pygame.Rect(player_start_x,player_start_y,ship_width,ship_height)
    while run:
        for event in pygame.event.get():
            # print(event)
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                break
                

            if event.type==pygame.KEYUP:
                if keys[pygame.K_SPACE]:
                    bullet=pygame.Rect(red.x+red.width/2,red.y,10,5)
                    all_bullets.append(bullet)
                    

        keys=pygame.key.get_pressed()
        movement(keys,red)




        # root.fill((255,255,0))
        root.blit(bg,(0,0))
        root.blit(player1,(red.x,red.y))
        # player2=pygame.draw.rect(root,(255,0,255),(800,0,100,500))
        if len(all_bullets)>0:
            for bullet in all_bullets:
                pygame.draw.rect(root,(255,0,0),bullet)
        bullet_movement()
        # bullet_movement(player2)


        ###TESTING###
        get_enemy_coords()


        draw_enemies()

        end_level()
        ###TESTING###



        score_text=text.render(f"Score:{score}",1,(255,255,255))
        root.blit(score_text,(10,10))

        health_text=text.render(f"Health:{health}",1,(255,255,255))
        root.blit(health_text,(width-health_text.get_width()-10,10))

        pygame.display.update()
        FPS.tick(60)

if __name__ == "__main__":

    main()