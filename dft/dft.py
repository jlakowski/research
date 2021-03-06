#A Discrete Fourier Transform
#Jim Lakowski
#10/04/2013

import numpy as np
import math
import time
#import matplotlib.pyplot as plt
import cmath
duration = 10 #length of the 
dtt = 0.01 #time inbetween samples
to = 0 #starting time
N = duration/dtt #total number of Time Samples

ds = 0.1 #difference in frequencies
so = -10

sf = 10
M = 2000 #total number of frequency samples
tstart = time.time()
#create t vector of the time steps
t = np.linspace(0, 100, N)
f = np.zeros(len(t))
#create the function for transforming
for a in range(0, len(t)):
    f[a] = math.cos(t[a]) + 0.5* math.cos(2*t[a])

#the transfer function is represented as an 
#M-dimensional vector 
F = np.zeros(M, dtype=np.complex)
s = np.linspace(so,sf, M)

for m in range(0, M):
    acc = complex(0) 
    #this is the integral 
    #it uses a right endpoint estimation
    for k in range(0, int(N)):
        tk = to + k*dtt
        arg = -2j * cmath.pi * s[m] * tk
        acc = acc + f[k]*cmath.exp(arg)*dtt
    F[m] = acc
tstop = time.time()
ttotal = tstop - tstart
print "total time in python %f seconds"%ttotal
"""
plt.figure(1)
plt.plot(t, f)
plt.show()


plt.figure(2)
plt.plot(s, F.real)
plt.show()

plt.figure(3)
plt.plot(s, F.imag)
plt.show()
"""
