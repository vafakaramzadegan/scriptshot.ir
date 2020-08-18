import tkinter as tk
import math

width = 900
height = 600

pend1_len = 150
pend2_len = 150

pend1_mass = 10
pend2_mass = 10

theta1 = math.pi/2
theta2 = math.pi

center_x = width / 2
center_y = 250

pend1_v = 0
pend2_v = 0

pend1_a = 0
pend2_a = 0

g = 2

lastX = 0
lastY = 0

air_ress_coef = 0.9999


firstLine = None
secondLine = None
first_pend = None
second_pend = None

root = tk.Tk()
root.title("Double Pendulum")

canvas = tk.Canvas(root,
                   width = width,
                   height = height,
                   highlightthickness=0)
canvas.pack(expand=1)

def simulate():
    
    global theta1
    global theta2
    global pend1_v
    global pend1_a
    global pend2_a
    global pend2_v
    global lastX
    global lastY
    global firstLine
    global secondLine
    global first_pend
    global second_pend

    pend1_a = (
            (-g * ((2 * pend1_mass) + pend2_mass) * math.sin(theta1)) 
            - 
            (pend2_mass * g * math.sin(theta1 - (2 * theta2)))
            -
            (2 * math.sin(theta1 - theta2) * pend2_mass)
            * 
            ((math.pow(pend2_v, 2) * pend2_len) + (math.pow(pend1_v, 2) * pend1_len * math.cos(theta1 - theta2)))
            ) / (pend1_len * ((2 * pend1_mass) + pend2_mass - (pend2_mass * math.cos((2 * theta1) - (2 * theta2)))))
    
    pend2_a = (2 * math.sin(theta1 - theta2)) * (
            (math.pow(pend1_v, 2) * pend1_len * (pend1_mass + pend2_mass)) +
            (g * (pend1_mass + pend2_mass) * math.cos(theta1)) +
            (math.pow(pend2_v, 2) * pend2_len * pend2_mass * math.cos(theta1 -theta2))
        ) / (pend2_len * (2 * pend1_mass + pend2_mass - (pend2_mass * math.cos((2 * theta1) - (2 * theta2)))))
    
    x1 = pend1_len * math.sin(theta1)
    y1 = pend1_len * math.cos(theta1)
    
    x2 = pend2_len * math.sin(theta2)
    y2 = pend2_len * math.cos(theta2)
    
    canvas.delete(firstLine)
    canvas.delete(secondLine)
    canvas.delete(first_pend)
    canvas.delete(second_pend)
    
    firstLine = canvas.create_line(center_x,
                       center_y,
                       center_x + x1,
                       center_y + y1,
                       fill = "#666",
                       width = 2)
    
    secondLine = canvas.create_line(center_x + x1,
                       center_y + y1,
                       center_x + x1 + x2,
                       center_y + y1 + y2,
                       fill = "#666",
                       width = 2)
    
    first_pend = canvas.create_oval(center_x + x1 - pend1_mass,
                       center_y + y1 - pend1_mass,
                       center_x + x1 + pend1_mass,
                       center_y + y1 + pend1_mass,
                       fill = "black")
    
    if lastX > 0:
        canvas.create_line(lastX,
                           lastY,
                           center_x + x1 + x2,
                           center_y + y1 + y2,
                           fill = "red", width = 2)
    
    second_pend = canvas.create_oval(center_x + x1 + x2 - pend2_mass,
                       center_y + y1 + y2 - pend2_mass,
                       center_x + x1 + x2 + pend2_mass,
                       center_y + y1 + y2 + pend2_mass,
                       fill = "black")
    
    pend1_v += pend1_a
    pend2_v += pend2_a

    theta1 += pend1_v
    theta2 += pend2_v
    
    #theta1 *= air_ress_coef
    #theta2 *= air_ress_coef
    
    lastX = center_x + x1 + x2
    lastY = center_y + y1 + y2

    canvas.after(25, simulate)

simulate()

root.mainloop()
