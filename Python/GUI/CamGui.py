#from compassbeta1 import getHeading
import sys
import multiprocessing
#added in for experimenting with compass graphics
import tkinter as tk
from tkinter import ttk

ENversion = "1.0" # Version of EchoNet

win = tk.Tk()

LARGE_FONT = ("Verdana", 12)

style = ttk.Style(win)
style.map("C.TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', 'blue'), ('active', 'blue')])

#Heading = getHeading()

class EchoNetApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "EchoNet "+ENversion)
        
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

        self.compassFrame = tk.Frame(self, height=300, width=300, bg='white')
        self.embed = tk.Frame(self.compassFrame, width=500, height=500)
        
        self.columnconfigure(0, pad=20)
        self.columnconfigure(2, pad=20)
        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=20)
        self.rowconfigure(2, pad=20)
                
        label1 = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label1.grid(row=0, column=1)

        self.label2 = tk.Label(self, text='0 s')
        self.label2.grid(row=3, column=1)

        button1 = ttk.Button(self, text="Device List",
                            command=lambda: controller.show_frame(DeviceList))
        button1.grid(row=1, column=0)
        
        button2 = ttk.Button(self, text="Track",
                            command=lambda: controller.show_frame(Track))
        button2.grid(row=4, column=0)
        
        button3 = ttk.Button(self, text="Mode",
                            command=lambda: controller.show_frame(Mode))
        button3.grid(row=1, column=2)
        
        button4 = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
        button4.grid(row=4, column=2)

        self.compassFrame.grid(row=2, column=1)

        #self.label3 = tk.Label(self, text='Waiting')
        #self.label3.grid(row=3, column=1)
        #self.label3.after(5, self.compassHeading)

        self.seconds = 0
        self.label2.after(1000, self.refresh_label)

    def refresh_label(self):
        self.seconds += 1
        self.label2.configure(text='%i s' % self.seconds)
        self.label2.after(1000, self.refresh_label)
        #self.label2.after(999, self.compassHeading)

    #def compassHeading(self):
        #self.Heading = getHeading()
        #self.label3.configure(text='%i degrees' % self.Heading)
        #self.label3.after(5, self.compassHeading)
        #self.label3.after(1, self.refresh_label)

class DeviceList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Device List")
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Track",
                            command=lambda: controller.show_frame(Track))
        button2.pack()
        
class Track(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Tracking")
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Device List",
                            command=lambda: controller.show_frame(DeviceList))
        button2.pack()
        
        
class Mode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Mode")
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Home", style="C.TButton",
                             command=lambda: controller.show_frame(HomePage))
        button1.pack()
        
class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Settings")
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        button1.pack()
        
app = EchoNetApp()
app.mainloop()

