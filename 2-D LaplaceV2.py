"""Overview
Austin Brandenberger
Setup:
Tub of water
Foil on the edges
circular bolt and rectangular angle iron inisde at 5V
Their position is defined on a grid system. 

Edge is at 0V
Bolt and angle iron is at 5V
using these initial conditions, I can utilize the method of relaxation (essentially averaging)
to find the electric potential at every spot inside the boundry

This code was adopted from "Computational Physics" by Mark Newman pgs 406-415

Completed Spring 2021 for 413 E&M II Honors
"""

import numpy as np
from pylab import imshow,gray, hot,show
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

n = 1
#multiplier
M = int(42*n) #grid from 0-43, so 44 if you count 0
N = int(23*n)#Real life grid from 0-23, so 24 if you count 0
# The method I am using to plot surfaces only likes square arrays
#but that does not fit my boundries. My data was taken in a 42x23
#grid, so a workaround is just averaging the points within Nprime,
#the points within my real life grid

"""Initial parameters to play with"""
#defining initial boundary conditions
vv = 0 #boundary voltage
V = np.zeros([M+1, M+1], float) 
V[0, :] = vv #boundary values at the top edge just for fun
Viron = 1

#defining my object(s) inside the boundary (places they take up on the grid)
#corners of angle Iron
#i = row
#j = column 
Ii0 = 23*n
Iif = 27*n
Ij0 = 4*n
Ijf = 20*n
V[Ii0:Iif+1, Ij0:Ijf+1] = Viron #setting angle Iron positions in my initial conditions grid to its voltage. 

#coordinates of the bolt on my Grid (there are 5 total points approximating it as a cross)
Vbolt = 5

Bitop = 4*n
Bibot = 6*n

Bimid = 5*n
Bjmid = 12*n

Bjleft = 11*n
Bjright = 13*n

V[Bitop:Bibot+1, Bjmid], V[Bimid, Bjleft:Bjright] = Vbolt, Vbolt #setting bolt positions in my initial conditions grid to its voltage. 

#array used to iterate and average
Vprime = np.zeros([M+1, M+1], float)


cts = 0
#This while loop keeps the grid values that correspond to the boundaries, the bolt and the angle iron at their respective
#voltages while repeatedly averaging every other value. 
while True: 
    for i in range(M):
        for j in range(N): 
            if i == 0 or i == M or j == 0 or j == N: #boundary values at the top/sides
                Vprime[i, j] = V[i, j]
            elif Ii0 <= i <= Iif and Ij0 <= j <= Ijf: #angle iron positions within the array
                Vprime[i, j] = V[i, j] = Viron
            elif Bitop<= i <=Bibot and j == Bjmid or i == Bimid and Bjleft<= j <= Bjright: #bolt positions within the array
                Vprime[i, j] = V[i, j] = Vbolt
            else: #values to be averaged
                    Vprime[i, j] = (V[i+1, j] + V[i-1, j] + V[i, j+1] + V[i, j-1])/4
                           
    V, Vprime = Vprime, V #switch the arrays
    cts += 1
    if cts == 1000: #runs the loop n times
        imshow(V)
        hot()
        show()
        break

   
"""
#If I want to run this with a much larger array it takes longer and I might want to see it later
#This saves off the array of stored voltage values and also imports it if needed
np.savetxt('0v.txt', V)
Vnew = np.loadtxt('0v.txt')
imshow(Vnew)
hot()
show()
"""

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#look at "surfaces" example code
#https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
X = np.linspace(0, M, M+1)
Y = np.linspace(0, M, M+1)
X, Y = np.meshgrid(X, Y)
Z = V
# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# Customize the z axis.
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()


