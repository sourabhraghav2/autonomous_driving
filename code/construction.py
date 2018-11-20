import math
import pygame
import random
# from code.vehicle import Vehicle
from code.calculation import *
from code.transformations import TransformCor

class Road:
    def __init__(self,turn_distance_list,screen,transformer,road_lane_color,front_loc,back_loc,road_width=25,display_middle=False,logger=False):
        self.turn_distance_list=turn_distance_list
        self.screen=screen
        self.transformer=transformer
        self.road_lane_color=road_lane_color
        self.road_width=road_width
        self.display_middle=display_middle
        self.logger=logger
        self.clock = pygame.time.Clock()
        self.front_loc=front_loc
        self.back_loc=back_loc
    def construct(self):
        paralel_distance = self.road_width



        self.front_loc = (50, 0)
        self.back_loc = (50, 30)


        if self.logger :print('a : ', self.front_loc)
        if self.logger :print('b : ', self.back_loc)
        r = None
        r_p_p_b_o=None
        l_p_p_b_o=None

        rotation_list=self.turn_distance_list
        total_len=len(rotation_list)
        for i in range(total_len):
            each=rotation_list[i]
            if i+1<total_len:
                next_angle= rotation_list[i+1][1]
            each_angle = each[1]
            distance = each[0]


            if self.logger :print('each_angle: ', each_angle)
            if r != None:
                #move to next line and storing previous
                self.front_loc = self.back_loc
                self.back_loc = r
            #rotate center line
            _, r = rotate_cord(self.back_loc, self.front_loc, each_angle, distance)

            if self.logger :print('b : ', self.back_loc)
            if self.logger :print('r : ', r)


            #generate parallel lines
            _, r_p_b = rotate_cord(self.back_loc, r, 270, paralel_distance)
            _, r_p_r = rotate_cord(r, self.back_loc, 90, paralel_distance)

            _, l_p_b = rotate_cord(self.back_loc, r, 270, -paralel_distance)
            _, l_p_r = rotate_cord(r, self.back_loc, 90, -paralel_distance)

            if next_angle != None:
                if self.logger :print('next_angle : ',next_angle)
                phi = 90 - (next_angle / 2)
                padding_distance = math.tan(math.radians(phi)) * paralel_distance
                padding_distance=math.sqrt(padding_distance*padding_distance)
                if self.logger :print('padding_distance: ',padding_distance)
                if next_angle < 180:
                    #right turn
                    #decrease right
                    r_p_r = find_cordinate_at(r_p_r, r_p_b, padding_distance)
                    #increase left
                    l_p_r = find_cordinate_at(l_p_r, l_p_b, -padding_distance)
                else:
                    #left turn
                    # decrease left
                    if self.logger :print('before : ', find_distance(l_p_r, l_p_b))
                    l_p_r = find_cordinate_at(l_p_r, l_p_b, padding_distance)
                    if self.logger :print('after : ', find_distance(l_p_r, l_p_b))
                    # increase right
                    r_p_r = find_cordinate_at(r_p_r, r_p_b, -padding_distance)


            #transform to reuired View
            b_o = self.transformer.transform(self.back_loc)
            r_o = self.transformer.transform(r)
            l_p_b_o =self. transformer.transform(l_p_b)
            l_p_r_o = self.transformer.transform(l_p_r)
            r_p_b_o = self.transformer.transform(r_p_b)
            r_p_r_o = self.transformer.transform(r_p_r)

            if r_p_p_b_o==None and l_p_p_b_o==None :
                r_p_p_b_o=r_p_b_o
                l_p_p_b_o=l_p_b_o

            pygame.draw.line(self.screen, self.road_lane_color, r_p_r_o, r_p_p_b_o)
            pygame.draw.line(self.screen, self.road_lane_color, l_p_r_o, l_p_p_b_o)
            if self.display_middle:pygame.draw.line(self.screen, (250, 234, 20), r_o, b_o)

            # self.clock.tick(15)

            #start from previous coordinates
            r_p_p_b_o = r_p_r_o
            l_p_p_b_o = l_p_r_o


            pygame.display.flip()