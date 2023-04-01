import tkinter as tk
from tkinter.messagebox import showinfo
import math
import random

import tools

RATIOHEXA = math.sqrt(3)/2

""" 
classe tile = canvas, polygon pour hexagon
classe frame = ensemble tiles, chacun une couleur et une callback
"""

class hexagonColorSelector(tk.Canvas):
    cSize = None
    tileRadius = 0
    brightness = 0
    hexaVertices = []

    lastSelectedTile = [0,0]

    def __init__(self, container, cSize=None, radius=7, brightness=1.2):
        tk.Canvas.__init__(self, container, width=cSize, height=cSize)
        self.pack()

        self.cSize = cSize
        self.tileW = self.cSize/(radius*2-1)
        self.tileRadius = self.tileW/(2*RATIOHEXA)
        self.brightness = brightness

        # drawing the middle line
        for i in range(2*radius-1):
            self._drawTile(self.tileW/2+i*self.tileW, cSize/2)

        for j in range(1,radius): # for each line upon/under the middle line
            xLine = (self.tileW/2)*(j+1)
            for i in range(2*radius-(1+j)): # for each hexagon per line
                yTile = cSize/2 - 1.5*self.tileRadius*j
                # drawing hexagons upon the middle line
                xTile = xLine+i*self.tileW
                self._drawTile( xTile, yTile)
                # drawing hexagons under the middle line
                yTile = cSize/2 + 1.5*self.tileRadius*j    
                self._drawTile(xTile, yTile)

        self.update()
        self.bind('<Button-1>', self.onColorSelectorClick)
        

    def _drawTile(self, x0, y0, state='Normal'):
        x = []
        y = []

        # Selecting the color
        theta = 3*math.atan2(y0-self.cSize/2,x0-self.cSize/2)/math.pi
        d = 1-self.brightness*2*math.sqrt((x0-self.cSize/2)**2+(y0-self.cSize/2)**2)/(self.cSize)
        d= min(1,max(0,d))

        color = self.getColorOnCircle(theta, d)

        # Selecting the vertices of the hexagon
        if state == 'Normal':
            radius = self.tileRadius
        if state == 'Selected':
            radius = self.tileRadius-2 # compensate the outline width
        for i in range(6) :
            angle = math.radians(i*360/6)
            x.append(int(x0+radius*math.sin(angle)))
            y.append(int(y0+radius*math.cos(angle)))

        # Drawing the hexagon
        if state == 'Normal':
            self.create_polygon(x[0],y[0],x[1],y[1],x[2],y[2],x[3],y[3],x[4],y[4],x[5],y[5], fill=color)
        if state == 'Selected':
            self.create_polygon(x[0],y[0],x[1],y[1],x[2],y[2],x[3],y[3],x[4],y[4],x[5],y[5], fill=color, outline=tools.darkenColor(color,0.8), width=2)
        
        # if x0==self.cSize/2 and y0==self.cSize/2:
        #     x = []
        #     y = []
        #     for i in range(6) :
        #         angle = math.radians(i*360/6)
        #         x.append(int(x0+self.tileRadius*0.95*math.sin(angle)))
        #         y.append(int(y0+self.tileRadius*0.95*math.cos(angle)))
        #     self.create_polygon(x[0],y[0],x[1],y[1],x[2],y[2],x[3],y[3],x[4],y[4],x[5],y[5], fill=color, outline=tools.darkenColor(color,0.8), width=2)
            

        self.hexaVertices.append([x0,y0])


    def getColorOnCircle(self, arg, mod):
        # choice of color depending on the angular position
        r = min(1, max(0, 2-abs(arg+3))) + min(1, max(0, 2-abs(arg-3)))
        g = min(1, max(0, 2-abs(arg+1)))
        b = min(1, max(0, 2-abs(arg-1)))

        
        # taking in account the distance from the center (brightness)
        r = round(255*min(1, max(0, r*(1-mod)+mod)))
        g = round(255*min(1, max(0, g*(1-mod)+mod)))
        b = round(255*min(1, max(0, b*(1-mod)+mod)))

        color = tools.rgb2hex(r,g,b)

        return color


    def onColorSelectorClick(self, event):
        x, y = event.x, event.y
        
        minDist=math.dist([x,y], self.hexaVertices[0])
        iMin = 0
        for i in range(1,len(self.hexaVertices)):
            dist = math.dist([x,y], self.hexaVertices[i])
            if dist < minDist:
                minDist = dist
                iMin = i
        if minDist<self.tileRadius:
            # Reset the last selected tile 
            if self.lastSelectedTile[0] != 0:
                self._drawTile(self.lastSelectedTile[0], self.lastSelectedTile[1], 'Normal')
            # Circle the new selected tile
            self._drawTile(self.hexaVertices[iMin][0], self.hexaVertices[iMin][1], 'Selected')
            # Update the last selected tile coordinates
            self.lastSelectedTile= [self.hexaVertices[iMin][0],self.hexaVertices[iMin][1]]







# Testing 
if __name__ == "__main__":
    size = 400

    app = tk.Tk()
    app.title('My Awesome App')
    app.geometry(str(size)+'x'+str(size))
    app.resizable(False, False)

    frame = hexagonColorSelector(app, size)

    app.mainloop()