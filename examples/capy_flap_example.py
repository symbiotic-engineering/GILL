import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import hydro
import numpy as np
import time
from matplotlib import pyplot as plt
from capy2dict import capy2dict

w = 18
t = 1
h = 10
draft = 9
cog = -0.7*h
omegas = np.linspace(0.2,5,20)
beta = 0
rho = 1025
depth = np.inf
stopwatch = []
for ii in range(1):
    start_time = time.time()
    data = hydro.run(w,t,h,draft,cog,omegas,beta,rho,depth)
    end_time = time.time()
    print(f'Total time: {end_time-start_time}')
    stopwatch.append(end_time-start_time)
print(np.mean(stopwatch))
print(data)
aspect = w/t
a_coef = 0.5547*np.exp(-0.0703*aspect)*aspect**(-0.3530) + 1
print(a_coef)
a33 = a_coef*rho*np.pi*(w/2)**2
z=np.linspace(0,draft,100)
dz = draft/100
Ainf = np.trapezoid(a33*(z**2)*dz,z)
Ainf = [[Ainf]]
hydro = capy2dict(data,w*t*draft,[0,0,0.5*draft],[0,0,cog],Ainf)
print(hydro["A"])
print(hydro["Ainf"])
plt.plot(omegas,np.reshape(hydro["A"],(len(omegas))))
plt.show()