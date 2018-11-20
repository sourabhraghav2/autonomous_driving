import pygame
import os
import numpy as np
from code.construction import Road
from code.transformations import TransformCor
from code.vehicle import Vehicle
from code.cardriver import  Driver


EPISODES=20000
if __name__ == "__main__":
    output_dir = 'model_output/carDriver/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    clock = pygame.time.Clock()

    win_height = 600
    win_width = 900
    front_loc = (50, 0)
    back_loc = (50, 30)

    screen = pygame.display.set_mode((win_width, win_height))
    transformer = TransformCor((win_height, win_width), 0, True)
    turn_distance_list = [(10, 180), (20, 180), (30, 180), (30, 160), (40, 160), (70, 160), (20, 180), (20, 190), (30, 200), (10, 190),
                          (20, 190), (20, 160), (20, 160), (20, 200), (20, 200), (50, 160), (40, 150), (30, 140),
                          (20, 130), (20, 160), (20, 200), (20, 200), (50, 160), (40, 150), (40, 210), (40, 210),
                          (40, 210), (40, 210), (40, 210), (40, 210), (20, 200), (50, 160), (40, 150), (30, 140),
                          (20, 130), (40, 210), (50, 160), (40, 150), (40, 210), (50, 160), (40, 150), (40, 210)]
    road = Road(turn_distance_list, screen, transformer, (25, 190, 20), front_loc, back_loc, road_width=35)
    road.construct()

    direction_list = {0: 160, 1: 170, 2: 180, 3: 190, 4: 200}

    car = Vehicle(screen, transformer, 8, back_loc, front_loc, 15, direction_list, padding_size=4, radar_range=30)
    #default moves
    car.set_of_moves([1, 4, 1, 2, 1])

    state_len = car.get_length_of_states()
    action_len= car.get_length_of_action()
    state_size = state_len
    action_size = action_len
    agent = Driver(state_size, action_size)
    agent.load(output_dir)
    done = False
    batch_size = 32

    click_detected = True
    for e in range(EPISODES):
        state = car.move(2)[0]
        state = np.reshape(state, [1, state_size])
        for time in range(6000):

            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP: click_detected = not click_detected

            while click_detected:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP: click_detected = not click_detected
                clock.tick(1)
                pygame.display.flip()


            action = agent.act(state)
            next_state, reward = car.move(action)
            print('reward : ', reward)
            done= True if(reward==-105) else False
            print('done : ',done)

            # next_state, reward, done, _ =car.move(action)
            # reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            clock.tick(10)
            pygame.display.flip()
            if done:
                car.vanish_car_chassis()
                print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, time, agent.epsilon))
                car = Vehicle(screen, transformer, 8, back_loc, front_loc, 15, direction_list, padding_size=4,
                              radar_range=30)
                # car.set_of_moves([2, 4, 2, 3, 2])
                road.construct()
                break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % 50 == 0 or e==EPISODES-1:
            agent.save(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")
        #
        if e==EPISODES-1:
            print('Bye!')