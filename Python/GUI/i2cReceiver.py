"""
SARNet
Author: Callum Munn-Middleton, Cameron Stauffer
Last Edited: November 22, 2019

Read I2C Bus
"""
from smbus2 import SMBus
import time
bus = SMBus(1)
address = 0x66

count = 0

while True: 
    
    data = bus.read_i2c_block_data(address, 0, 5)
    Packet1 = data[0] - 48
    Packet2 = data[1] - 48
    Packet3 = data[2] - 48
    Packet4 = data[3] - 48
    RSSI = data[4] * -1
    
    userID = str(Packet1)+str(Packet2)
    print('Packet is: ', Packet1, Packet2, Packet3, Packet4)
    print('RSSI is: {} dBm'.format(RSSI))
    print('User ID: ',userID)
    
    userID_write = '/home/pi/Documents/SARNet/GUI/RSSIuser_'+userID+'.txt'
    print('User ID File: ',userID_write)
    userID_file = open(userID_write,"w+")
    userID_file.write(str(RSSI))

    count+=1
    print('Count: ',count)
    print('*****************************************************************')

#     print('Packet: ', data1, data2, data3, data4)
#     print('rssi = ', rssi)
    time.sleep(0.5)
    
    
