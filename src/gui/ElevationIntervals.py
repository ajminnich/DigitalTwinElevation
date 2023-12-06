# Class: ElevationIntgervals.py
# Author: Alex Minnich but just contact John Morris (jhmmrs@clemson.edu). I've got no clue how this witchcraft works
# Date: 5 December 2023
# Purpose: modifying the simulation program to account for elevation
# Permissions: All rights reserved. Do not reuse without written permission from the owner. 

import matplotlib.pyplot as plt
import numpy as np

class Elevation:
    def __init__(self, mass, drive_force, x1, x2, theta1, theta2, theta3, x_coords):
        self.mass=mass
        self.drive_force=drive_force
        #self.time=time
        self.x1=x1
        self.x2=x2
        #self.x3=x3
        self.theta1=theta1
        self.theta2=theta2
        self.theta3=theta3
        self.x_coords=x_coords
        self.z_coords=[0]
        self.time=[0]
        self.time1=0
        self.time2=0
        self.time3=0
        self.z_tank1=0 
        self.z_tank2=0
        self.z_tank3=0
        self.z_old=0
        self.time_old=0
        self.fig, self.ax = plt.subplots()
        
        self.getTime()
        self.plotXZ()
        self.plotElevation()
        self.plotSetup()
      

        
    def plotSetup(self): #trying to use this to fix boundraries 
        plt.suptitle('Elevation Graph')
        plt.subplot(122)
        plt.xlabel('Horizontal Distance (m)')
        plt.xlim(0,self.x_max+self.x_max*0.05)
        plt.subplot(121)
        plt.suptitle('Elevation Graph')
        plt.xlabel('Time (s)')
        plt.ylabel('Height (m)')
        plt.xlim(0,self.time_max+self.time_max*0.05)
        plt.ylim(0,self.z_max+self.z_max*0.05)
        plt.show()

    def getTime(self):
        self.x_min=int(min(self.x_coords))
        self.x_max=int(max(self.x_coords))
        for i in range(self.x_min, self.x_max):  
            if i>=0 and i<=self.x1:
                self.elev_angle=self.theta1
                self.time_increase=np.sqrt((2*self.x_coords[i])/(9.81*np.cos(self.elev_angle*np.pi/180)))
            if i>self.x1 and i<=self.x2:
                self.elev_angle=self.theta2
                self.time_increase=np.sqrt((2*self.x_coords[i])/(9.81*np.cos(self.elev_angle*np.pi/180)))
            if i>self.x2 and i<=self.x_max:
                self.elev_angle=self.theta3
                self.time_increase=np.sqrt((2*self.x_coords[i])/(9.81*np.cos(self.elev_angle*np.pi/180))) 
            self.time_new=self.time_old+self.time_increase
            self.time_old=self.time_new
            self.time.append(self.time_new)
            

    def plotXZ(self):
        for i in range(self.x_min, self.x_max):  
            if i>=0 and i<=self.x1:
                self.elev_angle=self.theta1
                self.z_increase = .5*((self.drive_force)/(self.mass) - 9.81*np.cos(self.elev_angle*np.pi/180))*((1))**2 #currently set to 1 cause that's the step size. update in future versions
            if i>self.x1 and i<=self.x2:
                self.elev_angle=self.theta2
                self.z_increase = .5*((self.drive_force)/(self.mass) - 9.81*np.cos(self.elev_angle*np.pi/180))*(1)**2
            if i>self.x2 and i<=self.x_max:
                self.elev_angle=self.theta3
                self.z_increase = .5*((self.drive_force)/(self.mass) - 9.81*np.cos(self.elev_angle*np.pi/180))*((1))**2
            self.z_new=self.z_old+self.z_increase
            self.z_old=self.z_new
            self.z_coords.append(self.z_new)
            self.z_max=max(self.z_coords) 
            
            plt.subplot(122)
            plt.plot(self.x_coords[i],self.z_coords[i], '.', linewidth=1.0) #plots full elevation line
            plt.suptitle('Elevation Graph')
            plt.xlabel('Horizontal Distance (m)')
            plt.xlim(0,self.x_max+self.x_max*0.05)
            plt.pause(0.000001) ##temp cut for debugging time
        plt.plot(self.x_coords,self.z_coords, 'k-', linewidth=1.0) #plots full elevation line

    def plotElevation(self): #creates a line of the elevation to be climbed/descended vs elevation. Robot should follow this path
        self.time_max=max(self.time)
        plt.subplot(121)
        plt.plot(self.time, self.z_coords, 'g--', linewidth=1.0)
        plt.suptitle('Elevation Graph')
        plt.xlabel('Time (s)')
        plt.ylabel('Height (m)')
        plt.xlim(0,self.time_max+self.time_max*0.05)
        plt.ylim(0,self.z_max+self.z_max*0.05)
        #plt.show() 


test = Elevation(mass=5, x_coords=range(0, 50), x1=15, x2=30, theta1=30, theta2=5, theta3=50, drive_force=50)

print(test.z_coords)
