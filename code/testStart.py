import pygame
import random
from code.construction import Road
from code.transformations import TransformCor
from code.vehicle import Vehicle

clock = pygame.time.Clock()

win_height = 600
win_width = 900
front_loc = (50, 0)
back_loc= (50, 30)

screen = pygame.display.set_mode((win_width, win_height))
transformer = TransformCor((win_height, win_width), 0, True)
turn_distance_list=[(10, 180),(20, 180), (30, 180), (30, 160),(40, 150),(70, 160),(20, 200),(10, 200),(20, 200),(20, 160),(20, 160),(20, 200),(20, 200),(50, 160),(40, 150),(30, 140),(20, 130),(20, 160),(20, 200),(20, 200),(50, 160),(40, 150),(40, 210),(40, 210),(40, 210),(40, 210),(40, 210),(40, 210),(20, 200),(50, 160),(40, 150),(30, 140),(20, 130),(40, 210),(50, 160),(40, 150),(40, 210),(50, 160),(40, 150),(40, 210)]
road=Road(turn_distance_list,screen,transformer,(25, 190, 20),front_loc,back_loc,road_width=35)
road.construct()

direction_list={0: 160, 1: 170, 2: 180, 3: 190, 4: 200}

car = Vehicle(screen,transformer,8,back_loc,front_loc,15,direction_list,padding_size=4,radar_range=30)

state_len=car.get_length_of_states()
car.get_length_of_action()
car.set_of_moves([2,4,2,3,2])

click_detected=True
while True:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:click_detected=not click_detected

    if click_detected :states_and_rewards = car.move(int(random.randint(0, 4)))

    if states_and_rewards[1]<0:
        print('states_and_rewards : ',states_and_rewards)
        car.vanish_car_chassis()
        print('Vanish : ')
        car = Vehicle(screen, transformer, 8, back_loc, front_loc, 15, direction_list, padding_size=4, radar_range=30)
        car.set_of_moves([1,4,1,2,1])
    clock.tick(15)
    pygame.display.flip()



    clock.tick(1)
    print('Mouse ; ',pygame.mouse.get_pos())
    print('Pixel color : ', screen.get_at(pygame.mouse.get_pos()))

    pygame.display.flip()