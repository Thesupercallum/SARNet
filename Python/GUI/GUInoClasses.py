#!/usr/bin/python3 -i
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk
import subprocess
import time

### Variables ###

btnPadYhome = 70
btnPadY = 10
wPadX = 10
refreshFlag = False







def raise_frame(frame):
    frame.tkraise()
    
def quit_program():
    subprocess.run(['sudo', 'pkill', '-f', '/home/pi/Documents/SARNet/Compass/lsm303_Heading.py'])
    subprocess.run(['sudo', 'pkill', '-f', '/home/pi/Documents/SARNet/GUI/i2cReceiver.py'])
    subprocess.run(['sudo', 'pkill', '-f', '/home/pi/Documents/SARNet/Compass/compassTest2.py'])
    subprocess.run(['sudo', 'pkill', '-f', '/home/pi/Documents/SARNet/Sweep/sweepModule.py'])
    subprocess.run(['sudo', 'pkill', '-f', '/home/pi/Documents/SARNet/GUI/GUInoClasses.py'])
    
def restart_compass():
    subprocess.run(['sudo','pkill','-f','/home/pi/Documents/SARNet/Compass/compassTest2.py'])
    time.sleep(0.25)
    subprocess.run(['sudo','python3','/home/pi/Documents/SARNet/Compass/compassTest2.py'])

def restart_sweep():
    subprocess.run(['sudo','pkill','-f','/home/pi/Documents/SARNet/Sweep/sweepModule.py'])
    time.sleep(0.25)
    subprocess.run(['sudo','python3','/home/pi/Documents/SARNet/Sweep/sweepModule.py'])

def reboot_pi():
    subprocess.run(['sudo','reboot'])

def sweep_Start():
    print('Start Sweep Initialization')
    #sweepFlagInit = open('/mnt/GUI/sweepFlag', 'w+')
    sweepFlagInit = open('/home/pi/Documents/SARNet/GUI/sweepFlag', 'w+')
    print('sweepFlag opened')
    sweepFlagInit.write('1')
    print('Wrote 1 in sweepFlag')
    sweepFlagInit.close()
    print('Close sweepFlag')
    
    
def sweep_End():
    print('End Sweep Initialization')
    #sweepFlagEnd = open('/mnt/GUI/sweepFlag', 'w+')
    sweepFlagEnd = open('/home/pi/Documents/SARNet/GUI/sweepFlag', 'w+')
    print('sweepFlag opened')
    sweepFlagEnd.write('0')
    print('Wrote 0 in sweepFlag')
    sweepFlagEnd.close()
    print('Close sweepFlag')

def track_pressed():
    global devIDMain
    global Cleared
    Cleared = 0
    print('Entered track_pressed()')
    devIDMain = DevList.get(DevList.curselection())
    devIDMain = devIDMain[:-1]
    print('devIDMain Value: ',devIDMain)   
    RSSI_first = open('/home/pi/Documents/SARNet/GUI/RSSIuser_'+devIDMain+'.txt')
    RSSI_first.write('0')
    RSSI_file.close()
    track_ID(devIDMain)

def tracking_check():
    print('Cleared is: ', Cleared)
    if Cleared == 1:
        CurTrackID_Home = ttk.Label(fHomeRead, text=' --     ').grid(row=0, column=1, sticky='WE')
        CurTrackID_Swp = ttk.Label(fSwpRead, text=' --     ').grid(row=0, column=0, sticky='WE')    
        CurTrackID_Dev = ttk.Label(fDevRead, text=' --     ').grid(row=0, column=0, sticky='WE')
        CurTrackID_Set = ttk.Label(fSetRead, text=' --     ').grid(row=0, column=0, sticky='WE')
        CurRSSI_Home = ttk.Label(fHomeRead, text=' --     ').grid(row=1, column=1, sticky='SE')
        CurRSSI_Swp = ttk.Label(fSwpRead, text=' --     ').grid(row=1, column=0, sticky='W')
        CurRSSI_Dev = ttk.Label(fDevRead, text=' --     ').grid(row=1, column=0, sticky='W')
        CurRSSI_Set = ttk.Label(fSetRead, text=' --     ').grid(row=1, column=0, sticky='W')
    else:
        track_ID(devIDMain)

    
def track_ID(devIDMain):
    print('Entered track_ID')
    #print('TrackingFlag: ',TrackingFlag)

    #devIDMain = DevList.curselection()
    #CurTrackID_Home = Label(HomePage, text=devIDMain).grid(row=0, column=1, sticky='W')

    """devIDMain = DevList.get(DevList.curselection())
    print('Selecting Dev ID')
    """
    print(devIDMain)
    
    #print(devIDMain)
    
    #RSSI_file = open('/mnt/GUI/RSSIuseR_'+devIDMain+'.txt', 'w+')
    RSSI_file = open('/home/pi/Documents/SARNet/GUI/RSSIuser_'+devIDMain+'.txt')
    RSSIread = RSSI_file.readline()
    RSSI_file.close()
    
    RSSILength = len(RSSIread)
    
    if RSSILength == 3:
        newLength = RSSILength+2
        RSSIread = RSSIread.ljust(newLength)
        
    elif RSSILength == 2:
        newLength = RSSILength+4
        RSSIread = RSSIread.ljust(newLength)
    
    #print('Opening activeDevID file')
    #actDevID_file = open('/mnt/GUI/active')
    actDevID_file = open('/home/pi/Documents/SARNet/GUI/activeDevID', 'w')
    actDevID_file.write(devIDMain)
    #print('Wrote devIDMain to activeDevID file')
    actDevID_file.close()
    #print('Closed activeDevID\n')

    CurTrackID_Home = ttk.Label(fHomeRead, text=str(devIDMain)).grid(row=0, column=1, sticky='WE')
    CurTrackID_Swp = ttk.Label(fSwpRead, text=devIDMain).grid(row=0, column=0, sticky='WE')    
    CurTrackID_Dev = ttk.Label(fDevRead, text=devIDMain).grid(row=0, column=0, sticky='WE')
    CurTrackID_Set = ttk.Label(fSetRead, text=devIDMain).grid(row=0, column=0, sticky='WE')
    CurRSSI_Home = ttk.Label(fHomeRead, text=str(RSSIread)).grid(row=1, column=1, sticky='SE')
    CurRSSI_Swp = ttk.Label(fSwpRead, text=RSSIread).grid(row=1, column=0, sticky='W')
    CurRSSI_Dev = ttk.Label(fDevRead, text=RSSIread).grid(row=1, column=0, sticky='W')
    CurRSSI_Set = ttk.Label(fSetRead, text=RSSIread).grid(row=1, column=0, sticky='W')



    #lHomeTrack.configure(text=('Tracking: '+devIDMain))
    """
    CurRSSI_Home = Label(fHomeRead, text=str(RSSI_read)).grid(row=1, column=1, sticky='E')
    CurRSSI_Dev = Label(fDevRead, text=RSSI_read).grid(row=1, column=1, sticky='W')
    """
    #win.after(100, tracking_check)
    win.after(500, tracking_check)

    #print('End of track_ID: ',TrackingFlag)

    
def clear_ID():
    global Cleared
    Cleared = 1
    print('Entered clear_ID()')
    print('clear_ID Checkpoint: ',Cleared)

    
def dark_theme():
    #win = themed_tk.ThemedTk()
    #win.get_themes()
    win.set_theme("black")
    win.configure(bg='grey26')
    darkThemeFlag_file = open('/home/pi/Documents/SARNet/GUI/darkThemeFlag','w+')
    darkThemeFlag_file.write('1')
    print('Dark Theme Flag: 1')
    
    HomePage.configure(bg="grey26")
    HomePage.grid(row=0, column=0, sticky='NSEW')
    fHomeButton.configure(bg='grey26');fHomeData.configure(bg='grey26');fHomeTrack.configure(bg='grey26');fHomeRead.configure(bg='grey26')
    Sweep.configure(bg='grey26')
    fSwpButton.configure(bg='grey26');fSwpData.configure(bg='grey26');fSwpTrack.configure(bg='grey26');
    DeviceList.configure(bg='grey26')
    fDevButton.configure(bg='grey26');fDevData.configure(bg='grey26');fDevTrack.configure(bg='grey26');fDevInfo.configure(bg='grey26')
    Settings.configure(bg='grey26')
    fSetButton.configure(bg='grey26');fSetData.configure(bg='grey26');fSetTrack.configure(bg='grey26');fSetRead.configure(bg='26')

def light_theme():
    win.set_theme("scidblue")
    win.configure(bg='grey85')
    darkThemeFlag_file = open('/home/pi/Documents/SARNet/GUI/darkThemeFlag','w+')
    darkThemeFlag_file.write('0')
    print('Dark Theme Flag: 0')
    
    HomePage.configure(bg="grey85")
    HomePage.grid(row=0, column=0, sticky='NSEW')
    fHomeButton.configure(bg='grey85');fHomeData.configure(bg='grey85');fHomeTrack.configure(bg='grey85');fHomeRead.configure(bg='grey85')
    Sweep.configure(bg='grey85')
    fSwpButton.configure(bg='grey85');fSwpData.configure(bg='grey85');fSwpTrack.configure(bg='grey85');fSwpRead.configure(bg='grey85')
    DeviceList.configure(bg='grey85')
    fDevButton.configure(bg='grey85');fDevData.configure(bg='grey85');fDevTrack.configure(bg='grey85');fDevInfo.configure(bg='grey85')
    Settings.configure(bg='grey85')
    fSetButton.configure(bg='grey85');fSetData.configure(bg='grey85');fSetTrack.configure(bg='grey85');fSetRead.configure(bg='grey85')

def update_slider(value):
    #blVal = str(Set_blSlider.get())
    #Set_blVal.configure(text=value)
    print(value)
    

            ###############   Main   ###############
   
    
win  = themed_tk.ThemedTk()
win.get_themes()
win.set_theme("scidblue")
win.geometry('500x448+-10+0')
#win.wm_attributes('-type','splash')

print(ttk.Style().theme_names())

### Frame Declaration ###
HomePage = Frame(win)
#HomePage = Frame(win, bg='grey92')
fHomeButton = Frame(HomePage);fHomeData = Frame(HomePage);fHomeTrack = Frame(HomePage);fHomeRead=Frame(HomePage)

Sweep = Frame(win)
fSwpButton=Frame(Sweep);fSwpData=Frame(Sweep);fSwpTrack=Frame(Sweep);fSwpInfo=Frame(Sweep);fSwpRead=Frame(Sweep)

DeviceList = Frame(win)
fDevButton=Frame(DeviceList);fDevData=Frame(DeviceList);fDevTrack=Frame(DeviceList);fDevInfo=Frame(DeviceList);fDevRead=Frame(DeviceList)

Settings = Frame(win)
fSetButton=Frame(Settings);fSetData=Frame(Settings);fSetTrack=Frame(Settings);fSetRead=Frame(Settings)

for frame in (HomePage, Sweep, DeviceList, Settings):
    frame.grid(row=0, column=0, sticky='NSEW')

### Home Frames ###
fHomeButton.grid(row=2, column=0, sticky='S')
fHomeData.grid(row=2, column=1, sticky='N')
fHomeTrack.grid(row=1, column=0, sticky='NSE')
fHomeRead.grid(row=1, column=1, sticky='W')

### Devices Frames ###
fDevRead.grid(row=1, column=1, sticky='W')
fDevButton.grid(row=2, column=0, sticky='S')
fDevData.grid(row=2, column=1, sticky='N')
fDevTrack.grid(row=1, column=0, sticky='NSE')
#fDevInfo.grid(row=3, column=1, sticky='W')

### Settings Frames ###
fSetTrack.grid(row=1, column=0, sticky='NSE')
fSetRead.grid(row=1, column=1, sticky='W')
fSetButton.grid(row=2, column=0, sticky='S')
fSetData.grid(row=2, column=1, sticky='NE')

### Sweep Frames ###
fSwpTrack.grid(row=1, column=0, sticky='NSE')
fSwpRead.grid(row=1, column=1, sticky='W')
fSwpButton.grid(row=2, column=0, sticky='S')
fSwpData.grid(row=2, column=1, sticky='N')

### Settings Frames ###


            ###############   Home Page   ###############


### Home Page Frame ###
ttk.Label(HomePage, text='Home Page').grid(row=0, column=1)

Home_QuitBtn = ttk.Button(HomePage, text='Quit', command=lambda:quit_program())

Home_QuitBtn.grid(row=3, column=1)

### Home Page Tracking Frame ###
lHomeTrack = ttk.Label(fHomeTrack, text='Tracking: ').grid(row=0, column=0, sticky='E')
lHomeRSSI = ttk.Label(fHomeTrack, text='RSSI: ').grid(row=1, column=0, sticky='E')

### Home Page Data Frame ###
HomeData_file = open('/home/pi/Documents/SARNet/GUI/BatInstructions.txt')
batInstructions = HomeData_file.read()
HomeData_file.close()

sBarHome = tk.Scrollbar(fHomeData)
tBoxHome = tk.Text(fHomeData, height=20.5, width=42)
tBoxHome.insert('1.0', batInstructions)
tBoxHome.config(yscrollcommand=sBarHome.set, background='light grey', state=DISABLED)
sBarHome.config(command=tBoxHome.yview)

sBarHome.grid(row=0, column=0, sticky='NS')
tBoxHome.grid(row=0, column=0)

"""
sBarHome = tk.Scrollbar(fHomeData)
tBoxHome = tk.Text(fHomeData, height=22, width=42)
tBoxHome.pack(side=LEFT, fill=tk.Y)
sBarHome.pack(side=RIGHT, fill=tk.Y)
tBoxHome.config(yscrollcommand=sBarHome.set, background='light grey')
sBarHome.config(command=tBoxHome.yview)
tBoxHome.insert('1.0', batInstructions)
"""
### Button Frame (within Home Page Frame)
Home_HomeBtn = ttk.Button(fHomeButton, text='Home', command=lambda:raise_frame(HomePage))
Home_SweepBtn = ttk.Button(fHomeButton, text='Sweep', command=lambda:raise_frame(Sweep))
Home_DevBtn = ttk.Button(fHomeButton, text='Device List', command=lambda:raise_frame(DeviceList))
Home_SetBtn = ttk.Button(fHomeButton, text='Settings', command=lambda:raise_frame(Settings))

Home_HomeBtn.pack(pady=btnPadYhome, padx=wPadX, fill='x')
Home_SweepBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Home_DevBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Home_SetBtn.pack(pady=btnPadY, padx=wPadX, fill='x')


            ###############   Sweep Frame   ###############


### Sweep Frame ###
ttk.Label(Sweep, text='Sweep').grid(row=0, column=1)

### Sweep Tracking Frame ###
lSwpTrack = ttk.Label(fSwpTrack, text='Tracking: ').grid(row=0, column=0, sticky='E')
lSwpRSSI = ttk.Label(fSwpTrack, text='RSSI: ').grid(row=1, column=0, sticky='E')

### Sweep Button Frame ###
Swp_HomeBtn = ttk.Button(fSwpButton, text='Home', command=lambda:raise_frame(HomePage))
Swp_SweepBtn = ttk.Button(fSwpButton, text='Sweep', command=lambda:raise_frame(Sweep))
Swp_DevBtn = ttk.Button(fSwpButton, text='Device List', command=lambda:raise_frame(DeviceList))
Swp_SetBtn = ttk.Button(fSwpButton, text='Settings', command=lambda:raise_frame(Settings))

Swp_HomeBtn.pack(pady=btnPadYhome, padx=wPadX, fill='x')
Swp_SweepBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Swp_DevBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Swp_SetBtn.pack(pady=btnPadY, padx=wPadX, fill='x')

### Sweep Data Frame ###
Swp_Begin = ttk.Button(fSwpData, text='Begin Sweep', command=lambda:sweep_Start())
Swp_End = ttk.Button(fSwpData, text='End Sweep', command=lambda:sweep_End())

sBarSwp = tk.Scrollbar(fSwpData)
tBoxSwp = tk.Text(fSwpData, height=20.5, width=32)
tBoxSwp.insert('1.0', batInstructions)
tBoxSwp.config(yscrollcommand=sBarHome.set, background='light grey', state=DISABLED)
sBarSwp.config(command=tBoxSwp.yview)

sBarSwp.grid(row=0, column=0, sticky='NS')
tBoxSwp.grid(row=0, column=0)

Swp_Begin.grid(row=0, column=1, sticky='NW')
Swp_End.grid(row=0, column=1, sticky='SW')


            ###############   Device List Page   ###############


### Device List Frame ###
ttk.Label(DeviceList, text='Device List').grid(row=0, column=1)

### Device List Tracking Frame ###
ttk.Label(fDevTrack, text='Tracking: ').grid(row=0, column=0, sticky='NE')
ttk.Label(fDevTrack, text='RSSI: ').grid(row=1, column=0, sticky='SE')

### Device List Values Frame###


### Device List Button Frame ###
Dev_HomeBtn = ttk.Button(fDevButton, text='Home', command=lambda:raise_frame(HomePage))
Dev_SweepBtn = ttk.Button(fDevButton, text='Sweep', command=lambda:raise_frame(Sweep))
Dev_DevBtn = ttk.Button(fDevButton, text='Device List', command=lambda:raise_frame(DeviceList))
Dev_SetBtn = ttk.Button(fDevButton, text='Settings', command=lambda:raise_frame(Settings))

Dev_HomeBtn.pack(pady=btnPadYhome, padx=wPadX, fill='x')
Dev_SweepBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Dev_DevBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Dev_SetBtn.pack(pady=btnPadY, padx=wPadX, fill='x')

### Device List Data Frame ###
#DevData_file = open('/mnt/GUI/DevText.txt', 'w+')
DevData_file = open('/home/pi/Documents/SARNet/GUI/DevText.txt')
devText = DevData_file.read()
DevData_file.close()
#DevData_user = open('/mnt/GUI/user_00.txt', 'w+')
DevData_user = open('/home/pi/Documents/SARNet/GUI/user_00.txt')
devUName = DevData_user.readline()
devUSex = DevData_user.readline()
devUDate = DevData_user.readline()
devUTime = DevData_user.readline()
#DevList_file = open('/mnt/GUI/DeviceIDlist.txt', 'w+')
DevList_file = open('/home/pi/Documents/SARNet/GUI/DeviceIDlist.txt')
devID1 = DevList_file.readline()
devID2 = DevList_file.readline()
devID3 = DevList_file.readline()
devID4 = DevList_file.readline()

DevList = Listbox(fDevData, height=12, width=32)

DevList.insert(1, devID1)
DevList.insert(2, devID2)
DevList.insert(3, devID3)
DevList.insert(4, devID4)
DevList.grid(row=0, column=0)


"""
sBarDev = tk.Scrollbar(fDevData)
tBoxDev = tk.Text(fDevData, height=12, width=42)
tBoxDev.config(yscrollcommand=sBarDev.set, background='light grey')
sBarDev.config(command=tBoxDev.yview)
tBoxDev.insert('1.0', devText)
tBoxDev.grid(row=0, column=0)
sBarDev.grid(row=0, column=0, sticky='NS')
"""
Dev_StopBtn = ttk.Button(fDevData, text='Stop Track',
                         command=lambda:clear_ID())
Dev_TrackBtn = ttk.Button(fDevData, text='Track',
                          command=lambda:track_pressed())

nameLabel = ttk.Label(fDevData, text='Name: '+devUName)
sexLabel = ttk.Label(fDevData, text='Sex: '+devUSex)
dateLabel = ttk.Label(fDevData, text='Date Issued: '+devUDate)
timeLabel = ttk.Label(fDevData, text='Time Issued: '+devUTime)

nameLabel.grid(row=1, column=0, sticky='W')
sexLabel.grid(row=1, column=0, sticky='E')
timeLabel.grid(row=3, column=0, sticky='W')
dateLabel.grid(row=4, column=0, sticky='W')

Dev_StopBtn.grid(row=0, column=1, sticky='SW', padx=wPadX,)
Dev_TrackBtn.grid(row=0, column=1, sticky='NWE', padx=wPadX,)

#win.after(500, tracking_check())


            ###############   Settings Page   ###############


### Settings Frame ###
ttk.Label(Settings, text='Settings').grid(row=0, column=1)
#ttk.Button(Settings, text='Sweep', command=lambda:raise_frame(Sweep)).pack()
#ttk.Button(Settings, text='Home', command=lambda:raise_frame(HomePage)).pack()

### Settings Tracking Frame ###
ttk.Label(fSetTrack, text='Tracking: ').grid(row=0, column=0, sticky='NE')
ttk.Label(fSetTrack, text='RSSI: ').grid(row=1, column=0, sticky='SE')

### Settings Button Frame ###
Set_HomeBtn = ttk.Button(fSetButton, text='Home', command=lambda:raise_frame(HomePage))
Set_SweepBtn = ttk.Button(fSetButton, text='Sweep', command=lambda:raise_frame(Sweep))
Set_DevBtn = ttk.Button(fSetButton, text='Device List', command=lambda:raise_frame(DeviceList))
Set_SetBtn = ttk.Button(fSetButton, text='Settings', command=lambda:raise_frame(Settings))

Set_HomeBtn.pack(pady=btnPadYhome, padx=wPadX, fill='x')
Set_SweepBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_DevBtn.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_SetBtn.pack(pady=btnPadY, padx=wPadX, fill='x')

### Settings Data Frame ###
Set_blLabel = ttk.Label(fSetData, text='Brightness')

slider = IntVar()

Set_blSlider = ttk.Scale(fSetData, from_=0, to_=255, orient=HORIZONTAL, variable=slider, length=255,
                         command=lambda x:update_slider(x))

Set_darkTheme = ttk.Button(fSetData, text='Dark Theme',
                           command=lambda:dark_theme())
Set_lightTheme = ttk.Button(fSetData, text='Light Theme',
                            command=lambda:light_theme())
Set_restartComp = ttk.Button(fSetData, text='Restart Compass',
                             command=lambda:restart_compass())
Set_restartSweep = ttk.Button(fSetData, text='Restart Sweep',
                              command=lambda:restart_sweep())
Set_reboot = ttk.Button(fSetData, text='Reboot',
                        command=lambda:reboot_pi())

Set_blLabel.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_blSlider.pack(pady=1, padx=1, fill='x')
Set_darkTheme.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_lightTheme.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_restartComp.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_restartSweep.pack(pady=btnPadY, padx=wPadX, fill='x')
Set_reboot.pack(pady=btnPadY, padx=wPadX, fill='x')


#fSetData.after(50, update_slider())
#subprocess.run(['sudo','echo',blVal,'>','/sys/class/backlight/rpi_backlight/brightness'])

"""
sBarSet = tk.Scrollbar(fSetData)
tBoxSet = tk.Text(fSetData, height=20.5, width=32)
#tBoxSet = tk.Text(fSetData, height=20.5, width=42)
tBoxSet.insert('1.0', batInstructions)
tBoxSet.config(yscrollcommand=sBarSet.set, background='light grey', state=DISABLED)
sBarSet.config(command=tBoxSet.yview)
sBarSet.grid(row=0, column=0, sticky='NS')
tBoxSet.grid(row=0, column=0)
"""
### Start on Home Page ###
raise_frame(HomePage)
win.mainloop()
