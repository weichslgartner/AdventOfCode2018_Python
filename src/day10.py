import re
import numpy as np
from PIL import Image


points = []
vel = []
lines = open('../inputs/input_10.txt').readlines()
for line in lines:
    x,y, x_vel, y_vel = re.findall(r'-?\d+', line)
    points.append([int(x),int(y)])
    vel.append([int(x_vel),int(y_vel)])


points = np.array(points)
vel = np.array(vel)
width = 80
height = 15
for i in range(1,20000):
    points = np.add(points,vel)
    border_x_max = np.max(points[:, 0])
    border_y_max = np.max(points[:, 1])
    border_x_min = np.min(points[:, 0])
    border_y_min = np.min(points[:, 1])
    #print(border_x_max-border_x_min,border_y_max-border_y_min)
    #points = np.ceil(points, 20)
    #points = np.floor(points,0)
    found_width = border_x_max-border_x_min
    found_height = border_y_max - border_y_min
    if found_width < width and found_height < height:
        picture = np.zeros([height, width], dtype='uint8')
        for point in points:
            x = point[0] - border_x_min
            y = point[1] - border_y_min
            if 0 <= x< width and 0 <= y < height:
                picture[(y, x)]=255
        im = Image.fromarray(picture, mode='L')
        print(i)
        im.resize((400,400)).show()


#FPRRRZA