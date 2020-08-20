import tkinter as tk
import math

root = tk.Tk()
root.title("Fourier Series")

center_x = 200
center_y = 200

canvas = tk.Canvas(width = 800,
                   height = 400,
                   background = 'black',
                   highlightthickness=0)
canvas.pack(expand=1)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(center_x+x-r, center_y+y-r, center_x+x+r, center_y+y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_a_line(self, x1, y1, x2, y2, **kwargs):
    return self.create_line(center_x + x1, center_y + y1, center_x + x2, center_y + y2, **kwargs)
tk.Canvas.create_a_line = _create_a_line

deg = 0
wavData = []

def squareWave(i):
    n = i * 2 + 1
    return n, 4 / (n * math.pi)

def sawtoothWave(i):
    n = i + 1
    return n, 2 / ((-1 ** n) * n * math.pi)


def draw():
    global deg
    
    canvas.delete("all")
    
    x = 0
    y = 0
    prevX = 0
    prevY = 0
    count = 4
    
    for i in range(0, count):
        n, C = squareWave(i)
        radius = 100 * C
        canvas.create_circle(prevX, prevY, radius, outline = '#333', width = 1)
    
        x -= radius * math.cos(n * deg)
        y -= radius * math.sin(n * deg)

        canvas.create_circle(x, y, 4, fill = '#999', width = 1)   
        canvas.create_a_line(prevX, prevY, x, y, fill = "#333", width = 1)
        
        prevX = x
        prevY = y
    
    wavData.insert(0, y)
    
    for ind, data in enumerate(wavData):
        if ind < 1: continue
        canvas.create_a_line(ind,
                             wavData[ind - 1],
                             ind + 1,
                             data, fill = 'red', width = 2)
        
    canvas.create_a_line(x, y, 0, y, fill = "#666", width = 1)
    
    
    
    deg -= 0.1
    
    if len(wavData) > 500:
        del wavData[-1]
    
    canvas.after(20, draw)

draw()

root.mainloop()
