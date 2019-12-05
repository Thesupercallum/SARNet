#!/bin/bash -i
#EchoNet startup

sudo bash -c "/usr/bin/python3 /home/pi/Documents/SARNet/Compass/lsm303_Heading.py" &
sudo bash -c "usr/bin/python3 /home/pi/Documents/SARNet/GUI/i2cReceiver.py" &
sudo bash -c  "/usr/bin/python3 /home/pi/Documents/SARNet/GUI/GUInoClasses.py &"
sudo bash -c "/usr/bin/python3 /home/pi/Documents/SARNet/Compass/compassTest2.py &"
sudo bash -c "/usr/bin/python3 /home/pi/Documents/SARNet/Sweep/sweepModule.py" &
