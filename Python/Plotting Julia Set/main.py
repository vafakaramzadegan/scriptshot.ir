## Tutorial Video available on: https://www.aparat.com/v/brqn5

import tkinter as tk
from HSV import HSV_2_RGB

class JuliaSetApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mandelbrot Set")
        
        self.width = 300
        self.height = 300
        
        self.range_left = -2.0
        self.range_right = 2.0
        self.range_top = 2.0
        self.range_bottom = -2.0
        
        self.maxIterations = 30
        
        self.cx = 0
        self.cy = -0.8
        
        self.buildComponents()
        
        self.drawSet()
        
    def buildComponents(self):
        self.canvas = tk.Canvas(self.master,
                                width = self.width,
                                height = self.height,
                                background = 'black',
                                highlightthickness=0)
        self.canvas.pack(expand=1, side="top")
        self.canvas.bind("<Motion>", self.canvasMove)
        
    def canvasMove(self, event):
        self.cx = self.mapFromTo(event.x, 0, self.width, self.range_left, self.range_right)
        self.cy = self.mapFromTo(event.y, 0, self.height, self.range_bottom, self.range_top)
        
        self.drawSet()
        
        
        
    def mapFromTo(self, x, a, b, c, d):
        y = (x-a)/(b-a)*(d-c)+c
        return y
    
    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb
        
    def drawSet(self):
        for px in range(0, self.width - 1):
            #a = self.cx#self.mapFromTo(px, 0, self.width, self.range_left, self.range_right)
            for py in range(0, self.height - 1):
                #b = self.cy#self.mapFromTo(py, 0, self.height, self.range_top, self.range_bottom)
                
                x = self.mapFromTo(px, 0, self.width, self.range_left, self.range_right)
                y = self.mapFromTo(py, 0, self.height, self.range_top, self.range_bottom)
                
                iteration = 0
                
                while (x*x + y*y <= 2**2 and iteration < self.maxIterations):
                    xtemp = x*x - y*y + self.cx
                    y = 2*x*y + self.cy
                    x = xtemp
                    iteration += 1
                    
                hue = int (255 * (iteration / self.maxIterations))
                saturation = 255
                value = 255 if iteration < self.maxIterations else 0
                
                self.canvas.create_line(px, py, px+1, py, fill=self._from_rgb(HSV_2_RGB((hue, saturation, value))))
        
        
def main():
    root = tk.Tk()
    app = JuliaSetApp(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
