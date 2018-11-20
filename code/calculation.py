import math
def find_distance(origin, rotated):
    inner_distance = math.sqrt(
        (rotated[0] - origin[0]) * (rotated[0] - origin[0]) + (rotated[1] - origin[1]) * (rotated[1] - origin[1]))
    return inner_distance


def find_cordinate_at(origin, rotated, distance):
    inner_distance=find_distance(origin,rotated)
    t=distance/inner_distance
    # print('t : ',t)
    x=(1-t)*origin[0]+t*rotated[0]
    y=(1-t)*origin[1]+t*rotated[1]
    # print('x : ', x)
    # print('y : ', y)
    return int(x),int(y)

def rotate_cord(origin, initial, angel,distance):
    # print('origin: ',origin)
    # print('initial: ', initial)
    rotated = []
    rotated.append(origin[0]+(initial[0]-origin[0])*math.cos(math.radians(angel))-(initial[1]-origin[1])*math.sin(math.radians(angel)))
    rotated.append(origin[1]+(initial[0]-origin[0])*math.sin(math.radians(angel))+(initial[1]-origin[1])*math.cos(math.radians(angel)))
    return rotated,find_cordinate_at(origin,rotated,distance)

def rotate_on_len(radar,angle,radar_len):
    x = radar[0] + math.cos(math.radians(angle)) * radar_len
    y = radar[1] + math.sin(math.radians(angle)) * radar_len
    return x,y
