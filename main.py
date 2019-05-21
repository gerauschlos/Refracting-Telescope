import pygame as pg
import math

class Rays:
    
    def __init__(self,location,destination,destination1=None,destination2=None,destination3=None):
        self.location = location
        self.destination = destination
        self.destination1 = destination1
        self.destination2 = destination2
        self.destination3 = destination3
        self.movement = [(destination[0]-location[0])/60,(destination[1]-location[1])/60]
        self.x = location[0]
        self.y = location[1]

    def change_course(self,background):
        self.location = self.destination
        self.destination = self.destination1
        self.destination1 = self.destination2
        self.destination2 = self.destination3
        self.destination3 = None
        if self.destination == None: return
        self.movement = [(self.destination[0]-self.location[0])/60,(self.destination[1]-self.location[1])/60]
        self.x = self.location[0]
        self.y = self.location[1]

    def run(self,background):
        pg.draw.line(background,(255,255,0),[self.location[0],self.location[1]],[self.x,self.y],3)
        if self.x <= self.destination[0]: 
            self.x += self.movement[0]
            self.y += self.movement[1]
        else:   
            if self.destination1 != None:   self.change_course(background)

def mainh(height_object=70,distance_object=140,height_objective=300,height_ocular=150,distance_objective=400,distance_ocular=600):
    screen = pg.display.set_mode((1000,900), pg.RESIZABLE)

    pg.display.set_caption("Refracting Telescope")

    clock = pg.time.Clock()
    tree = pg.image.load("tree.png")
    tree = pg.transform.scale(tree, [height_object,height_object])
    tree = tree.convert()  
    
    
    center_curvature1 = [distance_objective+12, 450]
    center_curvature2 = [distance_ocular+12, 450]
    focal_objective1 = [distance_objective-int(height_objective/4)-25,450]
    focal_objective2 = [distance_objective+int(height_objective/4 + 50),450] 
    focal_ocular1 = [distance_ocular-int(height_ocular/4)-25,450] 
    focal_ocular2 = [distance_ocular+int(height_ocular/4+50),450]  

    final_destination = [focal_ocular2[0],focal_ocular2[1]]

    slope = [(focal_objective2[0]-center_curvature1[0])/60,(focal_objective2[1]-450-height_object)/60]
    x = focal_objective2[0]
    y = focal_objective2[1]
    while x < center_curvature2[0]:
        x+= slope[0]
        y-= slope[1]


    ray1 = Rays( [distance_object+int(height_object/2),450-height_object] , [center_curvature1[0],450-height_object] , [x,y] , final_destination)


    slope = [(distance_objective-int(height_objective/4)-(distance_object+int(height_object/2)))/60,(450-450-height_object)/60]
    x = distance_objective-int(height_objective/4) 
    y = 450
    while x < center_curvature1[0]:
        x += slope[0]
        y -= slope[1]

    ray2 = Rays ([distance_object+int(height_object/2),450-height_object],[x-25,y],[center_curvature2[0],y],final_destination)

    ray3 = Rays ([distance_object+int(height_object/2),450-height_object],center_curvature1,[center_curvature2[0],y],final_destination)
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((210 , 180 , 140))   
    
    pg.draw.line(background,(0,0,0),[100,450],[900, 450],3)# Boundary/Plane
    
    while True:
        clock.tick(60)     

        for event in pg.event.get():
            if event.type == pg.QUIT:   break

        image_formed = False

        objective = pg.draw.ellipse(background,(135, 206, 235),[distance_objective,450-int(height_objective*.5),25,height_objective],0)
        ocular = pg.draw.ellipse(background,(135, 206, 235),[distance_ocular,450-int(height_ocular*.5),25,height_ocular],0)
        pg.draw.circle(background,(0,0,0),center_curvature1,5)
        pg.draw.circle(background,(0,0,0),center_curvature2,5)
        pg.draw.circle(background,(0,0,0),focal_objective1,5)
        pg.draw.circle(background,(0,0,0),focal_objective2,5)
        pg.draw.circle(background,(0,0,0),focal_ocular1,5)
        pg.draw.circle(background,(0,0,0),focal_ocular2,5)


        ray1.run(background)
        ray2.run(background)
        ray3.run(background)

        if ray1.x >= float(final_destination[0]) and ray2.x >= float(final_destination[0]) and ray3.x >= float(final_destination[0]): break

        if ray1.y <= ray2.y: 
            image = pg.image.load("tree.png")
            intersection = [ray1.x,ray2.y]
            pg.transform.rotate(image,180)
            screen.blit(image, intersection)


        screen.blit(background, (0,0))
        screen.blit(tree, (distance_object, 450-height_object))

        pg.display.flip()

"""
from tkinter import *

root = Tk()
root.title("Refracting Telescope")
root.geometry("640x640+0+0")

heading = Label(root, text="Refracting Telescope Simulating", font=("arial",40,"bold"), fg="steelblue").pack()

name = StringVar()
entry_box = Entry(root, textvariable=name,width=25,bg="lightgreen").place(x=300,y=200)

def Submit():
    print(str(name.get()))

work = Button(root, text="Work",width=30,height=5,bg="lightblue",command=Submit).place(x=250,y=300)
"""

pg.quit()
