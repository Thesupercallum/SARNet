/* Simple Ping-Pong for a LoRa Radio/Modem
 *
 * In setup() below please adjust your country specific frequency ranges,
 * as well as the Bandwidth/SpreadingFactor/CodingRate settings.
 *
 * They way this example works is that the device first listens for 5000ms.
 * If it received a "PING" message, it considers itself a SLAVE. If not
 * it considers itself a MASTER. A SLAVE waits for an incoming "PING" message,
 * which it answers with a "PONG" message. A MASTER simply sends periodically
 * every 1000ms) a "PING" message, and collects "PONG" replies while waiting.
 *    
 *    
 * This example code is in the public domain.
 */
 
#include "LoRaRadio.h"
#include "Wire.h"

#define BME280_I2C_ADDRESS 0x66


char Info[3];
uint8_t tx_data[8];
int tx_index = 8;
int RssiSend = 0;

byte data = 0x00;

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
    LoRaRadio.setTxPower(14);
    LoRaRadio.setBandwidth(LoRaRadio.BW_125);
    LoRaRadio.setSpreadingFactor(LoRaRadio.SF_7);
    LoRaRadio.setCodingRate(LoRaRadio.CR_4_5);
    LoRaRadio.setLnaBoost(true);

    
    LoRaRadio.receive();


}

void loop( void )
{
 
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
              break;
            default:
              break;
          }
              tx_data[0] = Info[0];
              tx_data[1] = Info[1];
              tx_data[2] = Info[2];
              tx_data[3] = PacketStrength;
              Serial.print("RSSI: ");
              Serial.println(PacketStrength);
              Serial.print("Packet: ");
              Serial.println(Info);
              //Serial.print("TX Data: ");
              Serial.println(data);
              Wire.onRequest(SendData);
              RssiSend = PacketStrength * -1;
              Serial.println(RssiSend);
              
             
              
              
            
      }
    
}
void SendData()
{
   Wire.write(RssiSend);
   //Wire.write(Info[1]);

}
