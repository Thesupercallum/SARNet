
#include "LoRaRadio.h"
#include "Wire.h"

#define BME280_I2C_ADDRESS 0x66


byte Info[4];
int RssiSend = 0;
int info = 0;
int PacketSize = 0;
int PacketStrength = 0;

void setup( void )
{
    Serial.begin(9600);
    Wire.begin(BME280_I2C_ADDRESS);
    
    while (!Serial) { }

    LoRaRadio.begin(915000000);

    LoRaRadio.setFrequency(915000000);
    LoRaRadio.setTxPower(20);
    LoRaRadio.setBandwidth(LoRaRadio.BW_125);
    LoRaRadio.setSpreadingFactor(LoRaRadio.SF_7);
    LoRaRadio.setCodingRate(LoRaRadio.CR_4_5);
    LoRaRadio.setLnaBoost(true);
    LoRaRadio.receive();

}

void loop( void )
{
      LoRaRadio.receive();
      PacketSize = LoRaRadio.parsePacket();
      PacketStrength = LoRaRadio.packetRssi();
      if(PacketStrength < 0)
        {
          switch (PacketSize)
          {
            case 1:
              Info[0] = LoRaRadio.read();
              break;
            case 2:
              Info[0] = LoRaRadio.read();
              Info[1] = LoRaRadio.read();
              break;
            case 3:
              Info[0] = LoRaRadio.read();
              Info[1] = LoRaRadio.read();
              Info[2] = LoRaRadio.read();
            case 4:
              Info[0] = LoRaRadio.read();
              Info[1] = LoRaRadio.read();
              Info[2] = LoRaRadio.read();
              Info[3] = LoRaRadio.read();
              break;
            default:
              break;
          }
              //Serial.print("RSSI: ");
              //Serial.println(PacketStrength);
              //Serial.print("Packet: ");
              //Serial.println(Info);
              //Serial.print("TX Data: ");
              //Serial.println(data);
              RssiSend = PacketStrength * -1;
              Info[4] = RssiSend;

              if(Info[0] == 0 && Info[1] == 1 && Info[2] == 0)
              {
                LoRaRadio.beginPacket();
                LoRaRadio.write('A');
                LoRaRadio.endPacket();
              } 
              Wire.onRequest(SendData);   
         
      }
    
}
void SendData()
{
  Wire.beginTransmission(BME280_I2C_ADDRESS);
  Wire.write(Info[0]);
  Wire.write(Info[1]);
  Wire.write(Info[2]);
  Wire.write(Info[3]);
  Wire.write(RssiSend);
  Wire.endTransmission();

}
