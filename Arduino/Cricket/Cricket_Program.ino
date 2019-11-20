/*                Cricket Program
 *    This program is to be run on the Cricket device. It will have the 4 
 *    different modes that are able to be switched. Normal mode, Limp mode, 
 *    Alarm mode, and Distress mode.
 *    
 */


// Green LED is PA4 = Pin 18
// Red LED is PA3 = Pin 0
// Switch 1 is PA5 = Pin 21
// Swicth 2 is PA2 = Pin 1


#include "LoRaRadio.h"
#include "STM32L0.h"


//
#define SW1 21
#define SW2 1
#define RLED 0
#define GLED 18

#define Address 1       //Address can be set to 0-3 for different Crickets.

#define Normal 0        //Define modes to be able to switch between them.
#define Distress 1
#define Alarm 2
#define Limp 3

bool DistressState = 0;
bool AlarmState = 0;
bool LimpState = 0;
bool Wake_Flag = false;


int DeviceID = Address;
int Mode = 0;
int y = 0;
int z = 1;
int count = 0;


unsigned long SW1presstime = 0;
unsigned long SW2presstime = 0;
unsigned long aftertime = 0;

void setup() 
{

LoRaRadio.begin(915000000);
LoRaRadio.setFrequency(915000000);
LoRaRadio.setTxPower(20);
LoRaRadio.setBandwidth(LoRaRadio.BW_125);
LoRaRadio.setSpreadingFactor(LoRaRadio.SF_7);
LoRaRadio.setCodingRate(LoRaRadio.CR_4_5);
LoRaRadio.setLnaBoost(true);

pinMode(SW1, INPUT);
pinMode(SW2, INPUT);
pinMode(32, INPUT);

pinMode(RLED, OUTPUT);
pinMode(GLED, OUTPUT);

digitalWrite (RLED, LOW);
digitalWrite (GLED, LOW);

attachInterrupt(SW1, WakeyWakey, RISING);
attachInterrupt(SW2, WakeyWakey, RISING);
  

}

void loop() 
{
ButtonCheck();
//BatteryCheck();
if(Wake_Flag == true)
{
  Wake_Flag = false;
  attachInterrupt(SW1, WakeyWakey, RISING);
  attachInterrupt(SW2, WakeyWakey, RISING);
}

switch (Mode)
{
  case Normal:
    NormalMode();
    break;
  case Distress:
    DistressMode();
    break;
  case Alarm:
    AlarmMode();
    break;
  case Limp:
    LimpMode();
    break;
  default:
    break;
}
  
}

void NormalMode ()        //Function that runs while in normal operation. Cricket will sleep for 5 minutes then wake and send out its packet and go back to sleep.
{
  digitalWrite(GLED, HIGH);
  BuildPacket();
  delay(100);
  digitalWrite(GLED, LOW);
  delay(100);
  STM32L0.stop(300000);
}

void DistressMode ()      //Function that is entered in to by user of cricket to indicate trouble. 
{                         //Cricket will sleep for 1 minute then wake and send out its packet with distress indicator active and then go back to sleep.
  digitalWrite(RLED, HIGH);
  BuildPacket();
  delay(100);
  digitalWrite(RLED, LOW);
  STM32L0.stop(60000);
}

void AlarmMode()          //Function that is entered in to by a Bat module communicating with Cricket. Cricket will sleep for 10 seconds then wake up, send its packet and go back to sleep.
{
  Serial.print("Mode = Alarm");
  if(z == 1)
  {
    digitalWrite(GLED, HIGH);
    z = 0;
  }
  else
  {
    digitalWrite(RLED, HIGH);
    z = 1;
  }
  BuildPacket();
  digitalWrite(GLED, LOW);
  digitalWrite(RLED, LOW); 
  STM32L0.stop(10000);
}

void LimpMode()           //Function that is entered in to when the crickets battery liufe drops below a certain level. Cricket will sleep for 10 minutes then wake up, send its packet and go back to sleep.
{
  
  Serial.print("Mode = Limp");
  digitalWrite(RLED, HIGH);
  digitalWrite(GLED, HIGH);
  BuildPacket();
  delay(100);
  digitalWrite(RLED, LOW);
  digitalWrite(GLED, LOW);
  STM32L0.stop(600000);
}

void BatteryCheck()       //Function that checks the battery level of the Cricket.
{
// if(Vbat < 2.6)
// {
//  Mode = Limp;
//  LimpState = true;
// }
 
}

void BuildPacket()        //Function that builds the packet to be sent by the Cricket.
{
  char SendingPacket[3];
  switch(DeviceID)                //Checks device ID being used and inputs the correct values in position 0 and 1 of our packet array.
  {
    case 0:
      SendingPacket[0] = '0';
      SendingPacket[1] = '0';
      break;
    case 1:
      SendingPacket[0] = '0';
      SendingPacket[1] = '1';
      break;
    case 2:
      SendingPacket[0] = '1';
      SendingPacket[1] = '0';
      break;
    case 3:
      SendingPacket[0] = '1';
      SendingPacket[1] = '1';
      break;
  }
  if(AlarmState == 1)              //Checks the status of the LimpState variable and appends the packet to indicate if its in this state or not.
  {
    SendingPacket[2] = '1';
  }
  else
  {
    SendingPacket[2] = '0';
  }
  if(DistressState == 1)          //Checks the status of the DistressState variable and appends the packet to indicate if its in this state or not.
  {
    SendingPacket[3] = '1';
  }
  else
  {
    SendingPacket[3] = '0';
  }
  Serial.print("Built Packet: ");
  Serial.println(SendingPacket);
  SendPacket(SendingPacket);
}

void SendPacket(char SendingPacket[])         //Function that sends the built packet out through LoRa.
{
  LoRaRadio.beginPacket();
  for(int i = 0; i < 4; i++)
  {
    LoRaRadio.write(SendingPacket[i]);        //Sends each character individually of the packet array.
  }
  LoRaRadio.endPacket(true);
  delay(100);
  LoRaRadio.receive(1000);  //Listens for a response for a Bat.


  
  LoRaRadio.receive(1000); 
  if(LoRaRadio.parsePacket() == 1 && LoRaRadio.read() == 'A')         //Changes to Alarm mode if it hears from a Bat.
  {
    Mode = Alarm;
    AlarmState = true;
  }
  else
  {
   
  }

  
}

void ButtonCheck()
{
  while(digitalRead(SW1) == 1)
  {
    digitalWrite(GLED, HIGH); 
  }
  digitalWrite(GLED, LOW);
  if(digitalRead(SW2) == 1 && y == 0)
  {
    SW2presstime = millis();
    aftertime = SW2presstime + 5000;
    y = 1;
  }
  while(digitalRead(SW2) == 1)
  {
    if(digitalRead(SW1) == 1 && millis() > aftertime)
    {
      count = count + 1;
      delay(500);
    }
    if(count == 3)
    {
      Mode = Distress;
      DistressState = true;
      count = 0;
    }
  }
}

void WakeyWakey()
{
  Wake_Flag = true;
  STM32L0.wakeup();
}
