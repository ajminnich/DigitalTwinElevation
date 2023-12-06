# Class: TankAnimatorElevation.py
# Author: Alex Minnich(ish) but just contact John Morris (jhmmrs@clemson.edu). I've got no clue how this witchcraft works
# Date: 29 Oct 2023
# Purpose: modifying the simulation program to account for elevation
# Permissions: All rights reserved. Do not reuse without written permission from the owner. 

import matplotlib.pyplot as plt
import numpy as np

from src.gui.BlitManager import BlitManager
from src.gui.DrawTank import *
from src.objects.Tank import Tank

class TankAnimatorElevation:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "tank": self.tank = value
            if key == "time": self.time = value
            if key == "port_rpm": self.port_rpm = value
            if key == "strb_rpm": self.strb_rpm = value
            if key == "elevation": self.elevation = value
            if key == "mass": self.mass = value

        if "tank" not in kwargs: self.tank = Tank()
        if "time" not in kwargs: self.time = list(np.arange(0, 5, 0.1))
        if "port_rpm" not in kwargs: self.port_rpm = [20 for z in self.time]
        if "strb_rpm" not in kwargs: self.strb_rpm = [20 for z in self.time]
        if "elevation" not in kwargs: self.elevation = 10 #degrees theta
        if "mass" not in kwargs: self.mass = 5.

        self.fig, self.ax = plt.subplots()
        self.patch_objects = list()
        self.line_objects = list()
        self.patches = list()
        self.lines = list()
        self.Drive = 10 #place holder force till I figure out the rpm conversion
        self.rpm_avg = (np.array(self.port_rpm)+np.array(self.strb_rpm))/2 #finding avg rpm for tank on xy plane
        self.z_coords = .5*(np.array(self.Drive)/np.array(self.mass) - 9.81*np.sin(self.elevation*180/np.pi))*np.array(self.time)**2
        self.x_coords = self.time
        self.z_coords = list(self.z_coords) #converting to list so it's the same format as time
        self.y_coords = self.z_coords
        self.getObjects()
        self.initializePlot()

        for a in self.patches:
            self.ax.add_patch(a)
        for a in self.lines:
            self.ax.add_line(a)
        all_artists = self.patches + self.lines
        self.bm = BlitManager(self.fig.canvas, all_artists)

        plt.show(block=False)
        plt.pause(.1)

    def getObjects(self):
        self.patch_objects.append(Chassis(self.tank))
        self.patch_objects.append(Tread(self.tank, "port"))
        self.patch_objects.append(Tread(self.tank, "strb"))
        self.patch_objects.append(FrontDot(self.tank))

        self.line_objects.append(Ridges(self.tank, 0., side="port"))
        self.line_objects.append(Ridges(self.tank, 0., side="strb"))
        self.getPatches()
        self.getLines()

    def getPatches(self):
        for a in self.patch_objects:
            self.patches.append(a.get_patch())
        
    def getLines(self):
        for a in self.line_objects:
            for b in a.get_lines():
                self.lines.append(b)

    def initializePlot(self):
        plot_width = self.tank.ch_width * 5 #Half the plot width
        self.ax.set_xlim(self.tank.x - plot_width, self.tank.x + plot_width) #Set Screen Limits
        self.ax.set_ylim(self.tank.y - plot_width, self.tank.y + plot_width)
        self.ax.set_aspect('equal', adjustable='box')     
        plt.suptitle('Differential Drive Simulation with Elevation')
        plt.xlabel('Time (s)')
        plt.ylabel('Z-Coordinate (cm)')

    def moveTank(self, port_rpm, strb_rpm, step_duration):
        ''' Moves the tank and updates the travel route'''
        self.tank.move(port_rpm, strb_rpm, step_duration) 
        self.x_coords.append(self.time)
        self.y_coords.append(self.z_coords) #changed push to append

    def plotElevation(self): #creates a line of the elevation to be climbed/descended. Robot should follow this path
        self.ax.plot(self.time, np.tan[self.elevation*180/np.pi], ls='-', lw=2, color='#228B22')

    def plotRoute(self):
        self.ax.plot(self.x_coords, self.y_coords, ls='--', lw=2, color="#F56600")

    def animate(self):
        for j in range(len(self.time)):
            if j == len(self.time) - 1: step_duration = self.time[j] - self.time[j-1]
            else: step_duration = self.time[j+1] - self.time[j]
            self.moveTank(self.port_rpm[j], self.strb_rpm[j], step_duration)
            self.plotRoute()
            for a in self.patch_objects:
                a.update()
            for a in self.line_objects:
                a.update(self.time[j])

            self.bm.update()
            plt.title("RPM: {:.2f}  Elevation Degree: {:.2f}".format(self.rpm_avg, self.elevation))
            plt.pause(0.001)

        plt.show(block=True)
