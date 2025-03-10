import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import hydro
import numpy as np
import time
import matlab.engine
from matplotlib import pyplot as plt
from capy2wecSim import capy2struct

future_eng = matlab.engine.start_matlab(background=True)

w = 18
t = 1
h = 10
draft = 9
cog = -0.7*h
omegas = np.linspace(0.2,5,2)
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

eng = future_eng.result()
hydro = eng.struct()
hydro = capy2struct(hydro,data,w*t*draft,[0,0,0.5*draft],[0,0,cog])

#plt.plot(omegas,np.reshape(hydro["A"],(len(omegas))))
#plt.show()

# change following line to the path of the addWecSimSource.m file
eng.run('/home/degoede/SEA/mdo_wd2/src/WEC-Sim/addWecSimSource.m',nargout=0)
eng.addpath('src')
hydro = eng.solveIRFs(hydro)
hydro = eng.normalizeBEM(hydro)