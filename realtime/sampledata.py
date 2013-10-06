#!/usr/bin/python
# Jim Lakowski  May 29, 2013
# a script that creates a series of points int the same format the
# mocap server would give. simulating a circle. 
import math
import sys

f = open('circle.txt', 'w')
r = 400
z = 0
x = 400
y = 0
nrotations = 4
theta = 0
phi = 0
line = ''
while theta < (nrotations * 2 * math.pi): 
    
    y = r*math.sin(theta)
    x = r*math.cos(theta)
    z = r/2*math.cos(phi)
    
    line = str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(0) + ' ' +  str(0) + ' ' + str(0) + '\n' 
    
    f.write(line)
    theta = theta + 0.017 #1 degree in radians
    phi = phi + 0.034
    
