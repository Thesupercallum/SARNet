# Simple demo of of the LSM303 accelerometer & magnetometer library.
# Will print the accelerometer & magnetometer X, Y, Z axis values every half
# second.
# Author: Tony DiCola
# License: Public Domain
import time
# Import the LSM303 module.
import Adafruit_LSM303
import math #added for heading math

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

# Alternatively you can specify the I2C bus with a bus parameter:
#lsm303 = Adafruit_LSM303.LSM303(busum=2)



def getHeading():
    #print('Printing accelerometer & magnetometer X, Y, Z axis values, press Ctrl-C to quit...')
    #def getheading():
    #while True:
        # added a variable declaration for some math used for basic heading
    angle =0
    heading =0
    compmagx =0
    compmagy =0

    Xcomp = (-816 + 384)/2
    Ycomp = (-535+ 632)/2
    Zcomp = (-573 + 583)/2

    # Read the X, Y, Z axis acceleration values and print them.
    accel, mag = lsm303.read()
    # Grab the X, Y, Z components from the reading and print them out.
    accel_x, accel_y, accel_z = accel
    mag_x, mag_y, mag_z = mag

    mag_x -= Xcomp
    mag_y -= Ycomp
    mag_z -= Zcomp

    print('Accel X={0}, Accel Y={1}, Accel Z={2}, Mag X={3}, Mag Y={4}, Mag Z={5}'.format(
          accel_x, accel_y, accel_z, mag_x, mag_y, mag_z))


    accXnorm = accel_x / (math.sqrt(math.pow(accel_x, 2) + math.pow(accel_y, 2) + math.pow(accel_z, 2)))
    accYnorm = accel_y / (math.sqrt(math.pow(accel_x, 2) + math.pow(accel_y, 2) + math.pow(accel_z, 2)))


    pitch = math.asin(accXnorm)
    roll = -(math.asin(accYnorm/math.cos(pitch)))

        
    magXcomp = mag_x*math.cos(pitch)+ mag_z*math.sin(pitch)
    magYcomp = mag_x*math.sin(roll)*math.sin(pitch) + mag_y*math.cos(roll)+mag_z*math.sin(roll)*math.cos(pitch)

         

    heading = (math.atan2(magYcomp, magXcomp)*180)/math.pi
    heading -= 18


    if heading < 0:
        heading += 360
    #q= multiprocessing.Queue()  #multiprococessing attempt
    #q.put(heading)          #load heading into allocate memory
    print('better heading', heading)
    print('accX norm', accXnorm)
    print('accY norm', accYnorm)
    #if heading >=  and heading <30:
    #    print('North')
    if heading >= 30 and heading <60:
        print('North East')        
    if heading >= 60 and heading <120:
        print('East')
    if heading >= 120 and heading <150:
        print('South East')
    if heading >= 150 and heading <210:
        print('South')
    if heading >= 210 and heading <240:
        print('South West')
    if heading >= 240 and heading <300:
        print('West')   
    if heading >= 300 and heading <330:
        print('North West')
    else:
        print('North')

    return heading

#time.sleep(0.25)

#getheading()
