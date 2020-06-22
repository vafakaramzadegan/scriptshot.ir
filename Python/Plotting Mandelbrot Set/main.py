import tkinter as tk
from HSV import HSV_2_RGB

class MandelbrotSetApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mandelbrot Set")
        
        self.width = 1200
        self.height = 1200
        
        self.range_left = -2.0
        self.range_right = 2.0
        self.range_top = 2.0
        self.range_bottom = -2.0
        
        self.maxIterations = 100
        
        self.buildComponents()
        
        self.drawSet()
        
    def buildComponents(self):
        self.canvas = tk.Canvas(self.master,
                                width = self.width,
                                height = self.height,
                                background = 'black',
                                highlightthickness=0)
        self.canvas.pack(expand=1, side="top")
        self.canvas.bind("<Button-1>", self.canvasClick)
        
    def canvasClick(self, event):
        clickedX = self.mapFromTo(event.x, 0, self.width, self.range_left, self.range_right)
        clickedY = self.mapFromTo(event.y, 0, self.height, self.range_top, self.range_bottom)
        
        xDist = abs(self.range_left) + abs(self.range_right)
        scale = (30 * xDist / 100) / 2
        
        self.range_left = clickedX - scale
        self.range_right = clickedX + scale
        self.range_top = clickedY + scale
        self.range_bottom = clickedY - scale
        
        self.drawSet()
        
        
        
    def mapFromTo(self, x, a, b, c, d):
        y = (x-a)/(b-a)*(d-c)+c
        return y
    
    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb
        
    def drawSet(self):
        for px in range(0, self.width - 1):
            a = self.mapFromTo(px, 0, self.width, self.range_left, self.range_right)
            for py in range(0, self.height - 1):
                b = self.mapFromTo(py, 0, self.height, self.range_top, self.range_bottom)
                
                x = 0
                y = 0
                
                iteration = 0
                
                while (x*x + y*y <= 2*2 and iteration < self.maxIterations):
                    xtemp = x*x - y*y + a
                    y = 2*x*y + b
                    x = xtemp
                    iteration += 1
                    
                hue = int (255 * (iteration / self.maxIterations))
                saturation = 255
                value = 255 if iteration < self.maxIterations else 0
                
                self.canvas.create_line(px, py, px+1, py, fill=self._from_rgb(HSV_2_RGB((hue, saturation, value))))
        
        
def main():
    root = tk.Tk()
    app = MandelbrotSetApp(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
