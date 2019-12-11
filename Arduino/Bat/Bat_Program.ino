/*          The Bat Program
    This program is used with a Bat SARNet device. It should be uploaded 
    to the PCB using the header and programmer provided. The program is 
    used to listen for particular Cricket signals and then write them
    over the i2c bus. It will also send back an alarm trigger if it gets
    a message from the correct Cricke being tracked.
*/

#include "LoRaRadio.h"
#include "Wire.h"

#define BME280_I2C_ADDRESS 0x66


byte Info[4];
int RssiSend = 0;
int info = 0;                               //Defines for global variables
int PacketSize = 0;
int PacketStrength = 0;

void setup( void )
{
    Serial.begin(9600);
    Wire.begin(BME280_I2C_ADDRESS);         //Begin the i2c connection and establish the address being used.
    
    while (!Serial) { }

    LoRaRadio.begin(915000000);             //Begin the LoRa setup to 915MHz for north america.

    LoRaRadio.setFrequency(915000000);
    LoRaRadio.setTxPower(20);
    LoRaRadio.setBandwidth(LoRaRadio.BW_125);
    LoRaRadio.setSpreadingFactor(LoRaRadio.SF_7);       //Setting that can be changed to sacrifice data rate for range.
    LoRaRadio.setCodingRate(LoRaRadio.CR_4_5);
    LoRaRadio.setLnaBoost(true);
    
    LoRaRadio.receive();                    //Start listening for LoRa signals.

}

void loop( void )
{         
      PacketSize = LoRaRadio.parsePacket();         //Parse packet recieved for length.
      PacketStrength = LoRaRadio.packetRssi();      //Get packet received RSSI value.
      if(LoRaRadio.read() == '*')                   //Check to make sure it is a SARNet packet being received.
        {   
          
          Info[0] = LoRaRadio.read();
          Info[1] = LoRaRadio.read();
          Info[2] = LoRaRadio.read();
          Info[3] = LoRaRadio.read();               //Build an array from the received values in the packet.
                             
          RssiSend = PacketStrength * -1;
          Info[4] = RssiSend;
          
          Wire.onRequest(SendData);                 //Write data to the i2c bus when a request if made by the pi.
          delay(100);
          if(Info[0] == '1' & Info[1] == '0' & Info[2] == '0')
          {
            LoRaRadio.beginPacket();
            LoRaRadio.write('A');
            LoRaRadio.endPacket();
            delay(100);
            LoRaRadio.beginPacket();                //Sends an alarm signal back to the Cricket if it is the correct Cricket being tracked.
            LoRaRadio.write('A');
            LoRaRadio.endPacket();
            delay(100);
            LoRaRadio.receive();
           }
         }
         else
         {
          Info[4] = 0;    
         }
      if(PacketSize > 0)

}
void SendData()                                 //Function that begins, writes, and ends the i2c transmission.
{
  Wire.beginTransmission(BME280_I2C_ADDRESS);
  Wire.write(Info[0]);
  Wire.write(Info[1]);
  Wire.write(Info[2]);
  Wire.write(Info[3]);
  Wire.write(RssiSend);
  Wire.endTransmission();

}
