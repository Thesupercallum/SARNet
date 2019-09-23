#include <U8x8lib.h>
#include <SPI.h>
#include <LoRa.h>

U8X8_SSD1306_128X64_NONAME_SW_I2C u8x8(15, 4, 16);

int txPower = 17; //change to 20 after
int counter = 0;
int counter2 = 0;
const int csPin = 18;
const int resetPin = 14;
const int irqPin = 26;

void setup() {
  
  u8x8.setFont(u8x8_font_chroma48medium8_r);
  u8x8.begin();
  u8x8.setPowerSave(0);
  
  Serial.begin(9600);
  while (!Serial);
  LoRa.setPins(csPin, resetPin, irqPin);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    delay(500);
  }
  //LoRa.setSyncWord(0xFF);

  u8x8.drawString(0,0, "Callums LoRa");
  u8x8.drawString(0,1, "Setup Ok");
  delay(2000);
  u8x8.clearLine(0);
  u8x8.clearLine(1);
  u8x8.drawString(0,0, "Callum's Heltech");
  
 
}

void loop() {
  //u8x8.clearLine(1);
  Serial.print("Sending packet: ");
  Serial.println(counter);
  char Screen[16];
  sprintf(Screen, "Sent Msg:%i", counter);
  u8x8.drawString(0,1, Screen);

  char Screen2[16];
  sprintf(Screen2, "Count:%i", counter2);
  u8x8.drawString(0,2, Screen2);

  // send packet
  LoRa.beginPacket();
  LoRa.print(counter);
  LoRa.endPacket();

  counter++;
  counter2++;
  /*if(counter == 10)
  {
    counter = 0;
  }
  */
  LoRa.setTxPower(txPower);
  delay(1000);

  
}
