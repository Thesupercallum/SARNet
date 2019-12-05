#!/usr/bin/python3
from compassbeta1 import getHeading
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
import subprocess

#win=tk.Tk()
#win.geometry('+150+150')

ENversion = "1.1" # Version of EchoNet

#win = themk(theme="ITFT1")
#win.get_themes()
#win.set_theme("clearlooks")

LARGE_FONT = ("Verdana", 12)
buttonFont = ("Verdana", 22)
"""
style = ttk.Style()
style.map("C.TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', 'blue'), ('active', 'blue')])

style.configure('my.TButton', font = ('Calibri', 14, 'bold', 'underline'),
                foreground = 'red')
"""
"""
style.theme_use('classic')
Style().theme_use()

print(Style().theme_use())
"""

class EchoNetApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.wm_title(self, "EchoNet "+ENversion)
        self.geometry('+150+150')
                
        container = tk.Frame(self)        
        container.pack(side="top", fill="both", expand = True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (HomePage, DeviceList, Track, Mode, Settings):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="NSEW")
        
        self.show_frame(HomePage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
                
def qf(param):
    print(param)
    

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #print(Style().theme_use())

        btnPadY = 10
        
        self.buttonFrame = tk.Frame(self, height=300, width=300)
        self.dataFrame = tk.Frame(self, height=250, width=300, bg='white')
        #self.embed = tk.Frame(self.compassFrame, width=500, height=250)          
        
        self.columnconfigure(0, pad=20)
        self.columnconfigure(1, pad=20)
        self.columnconfigure(2, pad=20)
        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=20)
        self.rowconfigure(2, pad=20)
                
        label1 = ttk.Label(self, text="Home Page", font=LARGE_FONT)

        self.label2 = tk.Label(self, text='0 s')

        button1 = ttk.Button(self.buttonFrame, text="Device List", style='my.TButton',
                            command=lambda: controller.show_frame(DeviceList))        
        button2 = ttk.Button(self.buttonFrame, text="Track",
                            command=lambda: controller.show_frame(Track))       
        button3 = ttk.Button(self.buttonFrame, text="Mode",
                            command=lambda: controller.show_frame(Mode))        
        button4 = ttk.Button(self.buttonFrame, text="Settings",
                            command=lambda: controller.show_frame(Settings))

        self.label3 = tk.Label(self, text='Waiting')

        self.buttonFrame.grid(row=1, column=0, sticky='S')
        self.dataFrame.grid(row=1, column=1)
        
        label1.grid(row=0, column=1)
        self.label2.grid(row=4, column=1)
        
        button1.grid(row=1, column=0, pady=btnPadY)
        button2.grid(row=2, column=0, pady=btnPadY)
        button3.grid(row=3, column=0, pady=btnPadY)
        button4.grid(row=4, column=0, pady=btnPadY)

        self.label3.grid(row=2, column=1)
        #self.label3.after(5, self.compassHeading)

        self.seconds = 0
        self.label2.after(1000, self.refresh_label)

    def refresh_label(self):
        self.seconds += 1
        self.label2.configure(text='%i s' % self.seconds)
        #self.label2.after(1000, self.refresh_label)
        self.label2.after(999, self.compassHeading)

    def compassHeading(self):
        self.Heading = getHeading()
        self.label3.configure(text='%i degrees' % self.Heading)
        #self.label3.after(5, self.compassHeading)
        self.label3.after(1, self.refresh_label)


class DeviceList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Device List")
        
        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button2 = ttk.Button(self, text="Track",
                            command=lambda: controller.show_frame(Track))

        label.pack(pady=10, padx=10)
        
        button1.pack()
        button2.pack()

        
class Track(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Tracking")
        
        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button2 = ttk.Button(self, text="Device List",
                            command=lambda: controller.show_frame(DeviceList))

        label.pack(pady=10, padx=10)

        button1.pack()
        button2.pack()
        
        
class Mode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Mode")
        
        button1 = ttk.Button(self, text="Home", style="C.TButton",
                             command=lambda: controller.show_frame(HomePage))

        label.pack(pady=10, padx=10)

        button1.pack()

        
class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Settings")
        
        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        
        label.pack(pady=10, padx=10)
        
        button1.pack()
        
app = EchoNetApp()
app.mainloop()
