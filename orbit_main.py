# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 01:37:25 2023

@author: 18019
"""
import sys
import pygame as py
import numpy as np
import math

def __main__():
    global SCALING_FACTOR
    SCALING_FACTOR = 10
    FPS = 60
    # Some constants
    WIDTH, HEIGHT = 1000, 1000
    SUN_MASS = SCALING_FACTOR * 200
    PLANET_ONE_MASS = 1
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    
    # initialize the window
    py.init()
    window = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)
    running = True
    
    # make my objects
    theSun = star(SUN_MASS, vector(500,500), vector(0,0))
    planet_One = planet(PLANET_ONE_MASS, vector(250,250), vector(SCALING_FACTOR * 0.1,SCALING_FACTOR * -0.1))
    planetList = [planet_One]
    
    planet_Two = planet(PLANET_ONE_MASS * 1, vector(400, 400), vector(SCALING_FACTOR * 0.2, SCALING_FACTOR * -0.1))
    planetList.append(planet_Two)
    
    planet_Three = planet(PLANET_ONE_MASS * 1, vector(600,600), vector(SCALING_FACTOR * -0.1, SCALING_FACTOR * 0.1))
    planetList.append(planet_Three)
    
    #plusScale = Rectangle(50, 50, 50, 50, RED)
    #minusScale = Rectangle(150, 50, 50, 50, BLUE)
    
    clock = py.time.Clock()
    
    while running:
        
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.VIDEORESIZE:
                new_width, new_height = event.size
                WIDTH, HEIGHT = new_width, new_height
                window = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)
                py.display.update()
            if event.type == py.KEYDOWN:

                #Program quits with escape
                if event.key == py.K_ESCAPE:
                    running = False
            """  
            if event.type == py.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    mouseX, mouseY = py.mouse.get_pos()
                    if plusScale.collidepoint(mouseX, mouseY):
                        SCALING_FACTOR += 1
                    if minusScale.collidepoint(mouseX, mouseY):
                        SCALING_FACTOR -= 1
        """
        # Calculate gravitational force and update planet position.
        for body in planetList:
            for second_body in planetList:
                if second_body != body:
                    body.gravity(second_body)
                    body.updatePosition()
            body.gravity(theSun)
            body.updatePosition()
        
        # Draw figures on screen
        window.fill(BLACK)
        py.draw.circle(window, RED, (theSun.position.x, theSun.position.y), 20)
        for i in planetList:
            py.draw.circle(window, BLUE, (i.position.x, i.position.y),8)
        #plusScale.draw(window)
        #minusScale.draw(window)
        py.display.update()
        
    py.quit()
    sys.exit()

# General object floating in space class
class stellar_object():
    def __init__(self, mass, position, vel):
        self.mass = mass
        self.position = position
        self.is_fixed = False
        self.velocity = vel
        
    def is_fixed(self):
        return self.is_fixed
    
    def change_fixed(self, condition):
        self.is_fixed = condition
        
    def changePosition(self, x,y):
        self.x = x
        self.y = y
        
    def updatePosition(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        
    def position(self):
        return self.x, self.y
    
    def gravity(self, other_object):
        #calculate direction of gravitational force
        gConstant = 0.1
        direction = vector(other_object.position.x - self.position.x, 
                                      other_object.position.y - self.position.y
                    )
        distance = math.sqrt(direction.x ** 2 + direction.y ** 2)
        
        #calculate magnitude of gravitational force
        grav = SCALING_FACTOR * (gConstant * self.mass * other_object.mass) / (distance ** 2)
        
        #normalize the direction vector
        direction.x = direction.x / distance
        direction.y = direction.y / distance
        
        #apply graviational force to velocity
        forceVector = vector(direction.x * grav, direction.y * grav)
        self.velocity.x += forceVector.x / self.mass
        self.velocity.y += forceVector.y / self.mass
        
# Planet specific class that inherits from parent stellar_object class
class planet(stellar_object):
    def __init__(self, mass, position, vel):
        super().__init__(mass, position, vel)

#Star specific class that inherits from parent stellar object class
class star(stellar_object):
    def __init__(self, mass, position, vel):
        super().__init__(mass, position, vel)
        self.is_fixed = True

#Was thinking I would do more math here but ended up doing it in the stellar object class...
class vector:
    def __init__(self, x, y):
        self.x = x
        self.y =y

class Rectangle(py.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x,y,width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self, surface):
        py.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        

__main__()
