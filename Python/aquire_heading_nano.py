#serial reading test code
#read compass data sent by arduino and write to a file

#SARNet compass aquisition code


import serial
import os
ser = serial.Serial('/dev/ttyACM0', 9600) #change to USB addresss on Pi! ACMO
os.chdir("/mnt/rd") #change to ramdisk directory
f= open("testdoc", "w+")

while 1: 
    if(ser.in_waiting >0):
        line = ser.readline()#was  ser.readline()
        #print(line)
        headingString = str(line)
        length = len(line)
        #print(length)
        if (length == 8):
            cutString = headingString[2:5] # cut string to only include integers
            print(cutString)#                print correct number of characters
            os.chdir("/mnt/rd")
            f= open("testdoc", "w+") #create or a file if it doesnt exist and open it
            f.write(cutString) #write corrected string to file in ramdisk
            f.close()   #close the file and make it available for acces in ramdisk
            
        elif (length == 7):
            cutString = headingString[2:4]
            os.chdir("/mnt/rd")
            f= open("testdoc", "w+")
            f.write(cutString) 
            f.close() 
            print(cutString)
            
        elif (length == 6):
            cutString = headingString[2:3]
            print(cutString)
            os.chdir("/mnt/rd")
            f= open("testdoc", "w+")
            f.write(cutString) 
            f.close() 
           
        