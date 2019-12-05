from tkinter import *
#import tkMessageBox
import tkinter

top = Tk()

Lb1 = Listbox(top)
Lb1.insert(1, 'Hello')
Lb1.insert(2, 'My')
Lb1.insert(3, 'Name')
Lb1.insert(4, 'Is')
Lb1.insert(5, 'Cam')

Lb1.pack()
mainloop()
