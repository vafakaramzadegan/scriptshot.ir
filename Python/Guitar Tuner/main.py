import tkinter as tk
import crepe
import pyaudio
import audioop
import numpy as np

width = 500
height = 500

def mapFromTo(x, a, b, c, d):
    return (x-a)/(b-a)*(d-c)+c

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

notes = {"E2":  82.40689,
         "F2":  87.30706,
         "F#2": 92.49861,
         "G2":  97.99886,
         "G#2": 103.8262,
         "A2":  110.0000,
         "A#2": 116.5409,
         "B2":  123.4708,
         "C3":  130.8128,
         "C#3": 138.5913,
         "D3":  146.8324,
         "D#3": 155.5635,
         "E3":  164.8138,
         "F3":  174.6141,
         "F#3": 184.9972,
         "G3":  195.9977,
         "G#3": 207.6523,
         "A3":  220.0000,
         "A#3": 233.0819,
         "B3":  246.9417,
         "C4":  261.6256,
         "C#4": 277.1826,
         "D4":  293.6648,
         "D#4": 311.1270,
         "E4":  329.6276
         }

master = tk.Tk()
master.title("Guitar Tuner")

canvas = tk.Canvas(master,
                   width = width,
                   height = height,
                   highlightthickness = 0)
canvas.pack(expand = 1)

p = pyaudio.PyAudio()

stream =p.open(format = pyaudio.paInt16,
               channels = 1,
               rate =  16000,
               input = True)

def listen():
    data = stream.read(1024)
    if data:
        soundData = np.frombuffer(data, dtype=np.int16)
        if audioop.rms(soundData, 2) > 200:
            time, freq, confidence, activation = crepe.predict(soundData, 16000, model_capacity="small", step_size = 40)
            recorded = freq[np.argmax(confidence)]
            
            note_key, note_freq = min(notes.items(), key=lambda x: abs(recorded - x[1]))
        
            diff = (note_freq - recorded)
            
            diff_color = int(mapFromTo(abs(diff), 0, 10, 0, 255))
            if diff_color > 255:
                diff_color = 255
                
            diff_color = _from_rgb((diff_color, 255 - diff_color, 0))
        
            canvas.delete("all")
            canvas.create_text(width/2, 20, fill="black", font="Verdana 20 bold", text="%.2f" % recorded)
            canvas.create_text(width/2, 50, fill="black", font="Verdana 12", text="%.2f" % diff)
            
            canvas.create_text(width/2, 150, fill=diff_color, font="Verdana 40 bold", text=note_key)
            
            
    canvas.after(5, listen)
    
listen()

master.mainloop()
