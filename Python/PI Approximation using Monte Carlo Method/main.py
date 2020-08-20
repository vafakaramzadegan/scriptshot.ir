import tkinter as tk
import random

root = tk.Tk()
root.title("Pi Approximation")

center_x = 300
center_y = 300

canvas = tk.Canvas(width = 600,
                   height = 600,
                   background = 'black',
                   highlightthickness=0)
canvas.pack(expand=1)

radius = 200

canvas.create_oval(center_x - radius,
                   center_y - radius,
                   center_x + radius,
                   center_y + radius,
                   outline = "white")
canvas.create_rectangle(center_x - radius,
                        center_y - radius,
                        center_x + radius,
                        center_y + radius,
                        outline = "white")

total = 0
inside = 0
label = None

def draw():
    for i in range(0, 30000):
        global label    
        global total
        global inside
        
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        
        total += 1
        
        if x**2 + y**2 > radius**2:
            color = "red"
        else:
            color = "green"
            inside += 1
        
        canvas.create_line(center_x + x,
                           center_y + y,
                           center_x + x + 1,
                           center_y + y,
                           fill = color)
    
    pi = 4 * (inside / total)
    
    canvas.delete(label)
    
    label = canvas.create_text(center_x, 40, fill="yellow", font=("Ubuntu", 40), text = "PI: %.10f" % pi)

    canvas.after(20, draw)

draw()

root.mainloop()
