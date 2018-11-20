import numpy as np
from code.calculation import rotate_cord, find_cordinate_at
import pygame

from bresenham import bresenham
class Vehicle:
    def __init__(self,screen,transformer,width,front_loc,back_loc,move_distance,direction_list,padding_size=4,radar_range=8):
        self.front_loc=front_loc
        self.back_loc=back_loc
        self.width = width
        self.screen=screen
        self.transformer = transformer
        self.radar_range = radar_range
        self.move_distance=move_distance
        self.direction_list=direction_list
        self.middle_radar_len=int(self.radar_range*1.5)
        self.prev_back_loc = None
        self.prev_front_loc = None
        self.padding_size=padding_size
        self.prev_left_top = None
        self.prev_right_top = None
        self.prev_right_bottum= None
        self.prev_left_bottum= None

        self.length_of_states=(2*radar_range)+self.middle_radar_len
        self.length_of_action=len(self.direction_list)

        self.prev_left_top_padding = None
        self.prev_right_top_padding = None
        self.prev_right_bottum_padding = None
        self.prev_left_bottum_padding = None
        self.boundry_color=(25, 190, 20)

    def get_length_of_action(self):
        return self.length_of_action

    def get_length_of_states(self):
        return self.length_of_states

    def set_of_moves(self,directions):
        for each_direction in directions:
            self.move(each_direction)

    def vanish_car_chassis(self):
        if self.prev_left_top != None and self.prev_right_top != None and self.prev_right_bottum != None and self.prev_left_bottum:
            self.draw_rectangle((0, 0, 0), self.prev_left_top, self.prev_right_top, self.prev_right_bottum,self.prev_left_bottum)

    def draw_rectangle(self, color, left_top, right_top, right_bottum, left_bottum):
        pygame.draw.line(self.screen, color,
                         self.transformer.transform(left_top),
                         self.transformer.transform(right_top))

        # left
        pygame.draw.line(self.screen, color,
                         self.transformer.transform(left_top),
                         self.transformer.transform(left_bottum))

        # right
        pygame.draw.line(self.screen, color,
                         self.transformer.transform(right_bottum),
                         self.transformer.transform(right_top))

        # back
        pygame.draw.line(self.screen, color,
                         self.transformer.transform(right_bottum),
                         self.transformer.transform(left_bottum))


    def draw_current_Padding(self):
        if self.prev_left_top_padding != None and self.prev_right_top_padding != None and self.prev_right_bottum_padding != None and self.prev_left_bottum_padding:
            self.draw_rectangle((0, 0, 0), self.prev_left_top_padding, self.prev_right_top_padding, self.prev_right_bottum_padding,self.prev_left_bottum_padding)
        self.draw_rectangle((25, 90, 220), self.left_top_padding, self.right_top_padding, self.right_bottum_padding, self.left_bottum_padding)

        self.prev_left_top_padding=self.left_top_padding
        self.prev_right_top_padding=self.right_top_padding
        self.prev_right_bottum_padding=self.right_bottum_padding
        self.prev_left_bottum_padding=self.left_bottum_padding

    def draw_current_chessis(self):
        if self.prev_left_top != None and self.prev_right_top != None and self.prev_right_bottum != None and self.prev_left_bottum:
            self.draw_rectangle((0, 0, 0), self.prev_left_top, self.prev_right_top, self.prev_right_bottum,self.prev_left_bottum)
        self.draw_rectangle((205, 10, 220), self.left_top, self.right_top, self.right_bottum, self.left_bottum)

        self.prev_left_top=self.left_top
        self.prev_right_top=self.right_top
        self.prev_right_bottum=self.right_bottum
        self.prev_left_bottum=self.left_bottum





    def draw_current_pos(self):
        if(self.prev_back_loc!=None and self.prev_front_loc!=None):
            #clear previous point
            pygame.draw.line(self.screen, (0, 0, 0), self.transformer.transform(self.prev_front_loc),self.transformer.transform(self.prev_back_loc))
        #print('current ')
        pygame.draw.line(self.screen, (20, 254, 200), self.transformer.transform(self.front_loc), self.transformer.transform(self.back_loc))
        self.prev_back_loc=self.back_loc
        self.prev_front_loc=self.front_loc

    def get_Position(self):
        return self.front_loc,self.back_loc

    def move(self,direction):
        if direction==None or direction not in self.direction_list:
            raise Exception("Invalid Direction")

        angle=self.direction_list[direction]

        _, moved_loc = rotate_cord(self.front_loc, self.back_loc, angle, self.move_distance)
        self.back_loc=self.front_loc
        self.front_loc=moved_loc
        self.calculate_dimensions()
        self.draw_current_chessis()

        # self.draw_current_pos()
        states=self.monitor_distance().tolist()
        rewards=self.calculate_rewards()
        # self.draw_current_Padding()
        return states,rewards

    def recognize_crash(self):
        front = list(bresenham(self.left_top_padding[0],
                               self.left_top_padding[1],
                               self.right_top_padding[0],
                               self.right_top_padding[1]))
        left = list(bresenham(self.left_top_padding[0],
                              self.left_top_padding[1],
                              self.left_bottum_padding[0],
                              self.left_bottum_padding[1]))

        right = list(bresenham(self.right_bottum_padding[0],
                                self.right_bottum_padding[1],
                               self.right_top_padding[0],
                               self.right_top_padding[1]))
        back = list(bresenham(self.right_bottum_padding[0],
                              self.right_bottum_padding[1],
                              self.left_bottum_padding[0],
                              self.left_bottum_padding[1]))
        total_padding_location = np.concatenate([left, right, back])
        border_pixel_color = []
        for each_location in total_padding_location:
            try :
                border_pixel_color.append(self.color_detector(self.screen.get_at(self.transformer.transform(each_location))))
            except:
                border_pixel_color.append(True)


        # print('border_pixel_color : ', border_pixel_color)
        for i in border_pixel_color:
            if i :return True
        return False


    def draw_text(self,text):
        self.screen.blit(text, (50, 50))
    def calculate_rewards(self):
        total_reward=(self.middle_radar_len + (2 * self.radar_range))
        if self.recognize_crash():

            rewards=-total_reward

            self.screen.set_at((50,50),  (255,0,0))
            self.screen.set_at((51,50), (255, 0, 0))
            self.screen.set_at((52,50), (255, 0, 0))
            self.screen.set_at((53,50), (255, 0, 0))

            # raise Exception('Crash')
        else:

            left=np.amax(self.left_binary_detector)
            middle= np.amax(self.middle_binary_detector)
            right= np.amax(self.right_binary_detector)
            self.screen.set_at((50, 50), (0,128,0))
            self.screen.set_at((51, 50), (0,128,0))
            self.screen.set_at((52, 50), (0,128,0))
            self.screen.set_at((53, 50), (0,128,0))
            rewards=total_reward-(left+middle+right)

        return rewards
    def color_detector(self,each):
        detect=False
        if each[0] == self.boundry_color[0]: detect= True;
        if each[1] == self.boundry_color[1]: detect= True;
        if each[2] == self.boundry_color[2]: detect= True;
        # print('Boundry color : ',self.boundry_color)
        # print(detect,' Color Match the boundry : ',each)
        return detect

    def convert_signal_to_binary(self,color_list):
        final_binary_list = []
        color_found_at = None

        for i in range(len(color_list)):
            each = color_list[i]
            if self.color_detector(each):
                color_found_at = i
                break;
            else :
                final_binary_list.append(0)

        if color_found_at!=None:


            for i in range(color_found_at, len(color_list)):
                invert = len(color_list)-i
                final_binary_list.append(invert)

        return final_binary_list

    def calculate_dimensions(self):
        front_loc = self.front_loc
        back_loc = self.back_loc
        _, self.left_top = rotate_cord(front_loc, back_loc, 90, int(self.width / 2))
        _, self.left_bottum = rotate_cord(back_loc, front_loc, 270, int(self.width / 2))
        _, self.right_top = rotate_cord(front_loc, back_loc, 270, int(self.width / 2))
        _, self.right_bottum = rotate_cord(back_loc, front_loc, 90, int(self.width / 2))

        self.left_top_padding=find_cordinate_at(self.left_top ,self.right_bottum,-self.padding_size)
        self.right_bottum_padding = find_cordinate_at(self.right_bottum, self.left_top, -self.padding_size)

        self.left_bottum_padding = find_cordinate_at(self.left_bottum, self.right_top, -self.padding_size)
        self.right_top_padding = find_cordinate_at(self.right_top, self.left_bottum, -self.padding_size)


    def monitor_distance(self):
        front_right = []
        front_middle = []
        front_left = []
        external_boundry_color=(25, 190, 20)
        ##########  middle radar ###########
        for i in range(self.middle_radar_len):
            middle_pixel = find_cordinate_at(self.front_loc, self.back_loc, -i-3)
            # self.screen.set_at(self.transformer.transform(middle_pixel), (200, 100, 244))
            try:
                front_middle.append(self.screen.get_at(self.transformer.transform(middle_pixel)))
            except:
                front_middle.append(external_boundry_color)

        ##########  right radar  ###########
        for i in range(self.radar_range):
            right_pixel = find_cordinate_at(self.right_top, self.right_bottum, -i-2)
            # self.screen.set_at(self.transformer.transform(right_pixel), (200, 100, 244))
            try :
                front_right.append(self.screen.get_at(self.transformer.transform(right_pixel)))
            except:
                front_right.append(external_boundry_color)
        ##########  left radar  ###########
        for i in range(self.radar_range):
            left_pixel = find_cordinate_at(self.left_top, self.left_bottum, -i-2)
            # self.screen.set_at(self.transformer.transform(left_pixel), (100, 50, 200))
            try :
                front_left.append(self.screen.get_at(self.transformer.transform(left_pixel)))
            except:
                front_left.append(external_boundry_color)

        # #print('front_right: ', len(front_right))
        self.right_binary_detector = self.convert_signal_to_binary(front_right)
        #print(len(self.right_binary_detector),' right : ',self.right_binary_detector)

        # #print('front_middle: ', len(front_middle))
        self.middle_binary_detector = self.convert_signal_to_binary(front_middle)
        #print(len(self.middle_binary_detector),' middle: ', self.middle_binary_detector)

        # #print('front_left: ', len(front_left))
        self.left_binary_detector = self.convert_signal_to_binary(front_left)
        #print(len(self.left_binary_detector),' left: ', self.left_binary_detector)

        if len(self.left_binary_detector)  ==len(self.right_binary_detector) ==self.radar_range and self.middle_radar_len == len(self.middle_binary_detector):
           return  np.concatenate([self.left_binary_detector,self.middle_binary_detector,self.right_binary_detector])
        else:
            raise Exception('States Dimensions are not correct')

    def eraise_previous(self):
        if self.prev_left_top!=None and self.prev_right_top !=None and self.prev_right_bottum!=None and self.prev_left_bottum!=None :
                pygame.draw.line(self.screen, (0, 0, 0),
                                 self.transformer.transform(self.prev_left_top),
                                 self.transformer.transform(self.prev_right_top))

                # left
                pygame.draw.line(self.screen, (0, 0, 0),
                                 self.transformer.transform(self.prev_left_top),
                                 self.transformer.transform(self.prev_left_bottum))

                # right
                pygame.draw.line(self.screen, (0, 0, 0),
                                 self.transformer.transform(self.prev_right_bottum),
                                 self.transformer.transform(self.prev_right_top))

                # back
                pygame.draw.line(self.screen, (0, 0, 0),
                                 self.transformer.transform(self.prev_right_bottum),
                                 self.transformer.transform(self.prev_left_bottum))

        

