# Class: ElevationUnifrom.py
# Author: Alex Minnich but just contact John Morris (jhmmrs@clemson.edu). I've got no clue how this witchcraft works
# Date: 5 Dec 2023
# Purpose: modifying the simulation program to account for elevation
# Permissions: All rights reserved. Do not reuse without written permission from the owner. 

import matplotlib.pyplot as plt
import numpy as np

class Elevation:
    def __init__(self, mass, drive_force, elev_angle, time):
        self.mass=mass
        self.drive_force=drive_force
        self.elev_angle=elev_angle
        self.time=time
        self.getZCoord()
        self.plotElevation()
        self.plotTank()
        self.fig, self.ax = plt.subplots()
        plt.figure()
        

    def getZCoord(self):
        self.z_coords = .5*(np.array(self.drive_force)/np.array(self.mass) - 9.81*np.sin(self.elev_angle*np.pi/180))*np.array(self.time)**2
    
    def plotElevation(self): #creates a line of the elevation to be climbed/descended vs elevation. Robot should follow this path
        
        plt.subplot(121)
        plt.plot(self.time, self.z_coords, 'g--', linewidth=1.0)
        plt.suptitle('Elevation Graph')
        plt.xlabel('Time (s)')
        plt.ylabel('Height (m)') 
        #plt.show() 
    
    def plotTank(self): #creates graph of robot position in x vs z and dot shows position based on time  
        self.t_max=len(self.time)
        self.x_coords=self.z_coords/(np.tan(self.elev_angle*np.pi/180))
        self.x_max=max(self.x_coords)
        self.z_max=max(self.z_coords)
        plt.subplot(121)
        plt.ylim(0,self.z_max+300)
        plt.subplot(122)
        plt.xlabel('Horizontal Distance (m)')
        plt.plot(self.x_coords, self.z_coords,'k-') #plots full elevation line
        for i in range(1,self.t_max): #want to update this to be more steps in the same bounds as time
            #plt.subplot(122)
            plt.axis((0,self.x_max+300,0,self.z_max+300))
            plt.plot(self.x_coords[i], self.z_coords[i],'.')
            plt.pause(0.000001) ##temp cut for debugging time
            plt.close(122)
        plt.subplot(122)
        plt.show()

test = Elevation(mass=5, drive_force=100, elev_angle=75,time=np.linspace(0, 20, 100)) #change last 20 to 100
print(test.z_coords)
