#!/usr/bin/env python
# coding=utf-8

# import rospy
import pygame
import pygame.locals
from pygame.locals import *
from socket import *

ZMQ_SERVER = "47.97.42.104"

FPS = 50
MAX_SPEED = 0.9
MIN_SPEED = -0.9
MAX_HEADING = 31  # right
MIN_HEADING = -31  # left
DELTA_SPEED = 0.04
DELTA_HEADING = 6
PORT = 8080
ip = "127.0.0.1"
recv_size = 2020

def render_label(text, screen):
    font = pygame.font.Font(None, 36)
    text = font.render(text, 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = screen.get_rect().centery

    screen.blit(text, textpos)

speed  = 0
angle = 0
s = {}
stear = 1
direction = 1

def clamp(m, m1, m2):
    if m < m1:
        return m1
    if m > m2:
        return m2
    return m

def send_commend(control_cmd):
    try:
        data = struct.pack('>iff', control_cmd, speed, angle) #1 为正常速度转角控制位 2为倒档 3为正档 4为active
        s.sendall(data)
        recv_data = s.recv(recv_size)
        print(recv_data)
    except:
        return False

def add_speed():
    if stear==1:
        return clamp(speed+0.1, 0, 2)
    elif stear==2:
        return clamp(speed+0.1, 0, 8)
    elif stear==3:
        return clamp(speed+0.1, 0, 12)
    elif stear==4:
        return clamp(speed+0.2, 0, 16)
    elif stear==5:
        return clamp(speed+0.2, 0, 20)

def sub_speed():
    if stear==1:
        return clamp(speed-0.05, 0, 2)
    elif stear==2:
        return clamp(speed-0.05, 0, 8)
    elif stear==3:
        return clamp(speed-0.05, 0, 12)
    elif stear==4:
        return clamp(speed-0.1, 0, 16)
    elif stear==5:
        return clamp(speed-0.2, 0, 20)

def turn(direction):
    if direction == 'l':
        return clamp(angle-0.1, -30, 30)
    elif direction == 'r':
        return clamp(angle+0.1, -30, 30)
    else:
        return 0


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Remote Control')
    pygame.display.flip()
    clock = pygame.time.Clock()
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((ip,PORT))
    while True:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_UP]:
            print("前左")
            angle = turn('l')
            if speed==0:
                send_commend(3)
            speed = add_speed()
        elif keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_UP]:
            print("前右")
            angle = turn('r')
            if speed==0:
                send_commend(3)
            speed = add_speed()
        elif keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_DOWN]:
            print("后左")
            angle = turn('l')
            if speed==0:
                send_commend(2)
            speed = add_speed()
        elif keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_DOWN]:
            print("后右")
            angle = turn('r')
            if speed==0:
                send_commend(2)
        elif keys_pressed[pygame.K_SPACE]:
            speed = 0
            angle = 0
            print('空格')
        elif keys_pressed[pygame.K_UP]:
            speed = add_speed()
            print('上键')
        elif keys_pressed[pygame.K_DOWN]:
            speed = add_speed()
            print('下键')
        else:
            speed = sub_speed()
            if keys_pressed[pygame.K_RIGHT]:
                angle = turn('l')
                print('右键')
            elif keys_pressed[pygame.K_LEFT]:
                angle = turn('r')
                print('左键')
            elif keys_pressed[pygame.K_a]:
                send_commend(4)
                continue
        if keys_pressed[pygame.K_LEFT]==False and keys_pressed[pygame.K_RIGHT]==False:
            if angle < 0:
                angle = min(angle+0.5, 0)
            if angle > 0:
                angle = max(angle-0.5, 0)

        send_commend(1)  
        pygame.event.pump()
        screen.fill(pygame.Color('white'))
        render_label('{}  V:{:.02f} H:{:.02f}'.format("Cloud Control:", speed, angle), screen)
        pygame.display.flip()
    print('end')