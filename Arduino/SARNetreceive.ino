#include <SPI.h>
#include <LoRa.h>
#include <U8x8lib.h>          //library for the screen
const int csPin = 18;          // LoRa radio chip select
const int resetPin = 14;       // LoRa radio reset
const int irqPin = 26;
int RecCount = 0;
U8X8_SSD1306_128X64_NONAME_SW_I2C u8x8(15, 4, 16); //generic screen driver

void setup() {
  u8x8.setFont(u8x8_font_chroma48medium8_r); //from online example
  u8x8.begin(); //initialize the screen.
  u8x8.setPowerSave(0);
  LoRa.setPins(csPin, resetPin, irqPin);// set CS, reset, IRQ pin
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Receiver");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  //LoRa.setSyncWord(0xFF);

  u8x8.drawString(0,0, "James LoRa"); // 0,0 = x y coordinates
  u8x8.drawString(0,1, "Setup OK"); // 0,0 = x y coordinates
  delay(2000);
  u8x8.clearLine(0);
  u8x8.clearLine(1);
  u8x8.drawString(0,0, "James's Heltech"); 
  
} //end of void setup


void loop() {
  //u8x8.clearLine(1);
  //u8x8.clearLine(2);
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    //Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      //Serial.print((char)LoRa.read());
      //int Info = ((char)LoRa.read() - 48);
      //char Info = LoRa.read();
      //Serial.print(Info);
      char Display[16];
      //String Info = (String)LoRa.read();
      char Info = LoRa.read();
      char Info2 = LoRa.read();
      char Info3 = LoRa.read();
      char Info4 = LoRa.read();
      sprintf(Display, "Got Msg: %c%c%c%c", Info, Info2, Info3, Info4);
      
      u8x8.drawString(0,1, Display);
      float rssi = LoRa.packetRssi();
      char Display2[16];
      sprintf(Display2, "Strength:%.1f", rssi);

      
      u8x8.drawString(0,2, Display2);

      char Display3[16];
      sprintf(Display3, "Count: %i", RecCount);
      u8x8.drawString(0,3, Display3);
      RecCount++;
      

           
    }

    // print RSSI of packet
    //Serial.print("' with RSSI ");
    //Serial.println(LoRa.packetRssi());
  }
}
