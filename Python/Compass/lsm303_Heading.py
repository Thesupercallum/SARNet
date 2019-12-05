import serial
import os
import sys
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)
os.chdir("/mnt/rd")
f = open("testdoc","w+")

while True:
    
        if(ser.in_waiting >0):
            line = ser.readline()#was  ser.readline()
            headingString = str(line)
            length = len(line)
            
            if (length == 8):
                
                cutString = headingString[2:5] # cut string to only include integers
                print(cutString)#                print correct number of characters
                os.chdir("/mnt/rd")
                f= open("testdoc", "w+") #create or a file if it doesnt exist and open it
                f.write(cutString) #write corrected string to file in ramdisk
                f.close()   #close the file and make it available for acces in ramdisk
                
                #return cutString
                
            elif (length == 7):
                
                cutString = headingString[2:4]
                os.chdir("/mnt/rd")
                f= open("testdoc", "w+")
                f.write(cutString) 
                f.close() 
                print(cutString)
               
                #return cutString
                
            elif (length == 6):
                
                cutString = headingString[2:3]
                print(cutString)
                os.chdir("/mnt/rd")
                f= open("testdoc", "w+")
                f.write(cutString) 
                f.close()

                #return cutString

            
        #time.sleep()