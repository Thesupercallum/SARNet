from smbus2 import SMBus
import time
bus = SMBus(1)
address = 0x66


    


while True: 
    
    data = bus.read_i2c_block_data(address, 0, 5)
    Packet1 = data[0] - 48
    Packet2 = data[1] - 48
    Packet3 = data[2] - 48
    Packet4 = data[3] - 48
    Rssi = data[4] * -1
    print('Packet is: ', Packet1, Packet2, Packet3, Packet4)
    print('Rssi is: ', Rssi)

      
#     print('Packet: ', data1, data2, data3, data4)
#     print('rssi = ', rssi)
    time.sleep(5)
    
    