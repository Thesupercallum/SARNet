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
bool LimpState = 0;               //Variables used to see the mode the cricket is in.
bool Wake_Flag = false;


int DeviceID = Address;
int Mode = 0;
int y = 0;                    //Global variables defined.
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
LoRaRadio.setSpreadingFactor(LoRaRadio.SF_7);         //Setup LoRa settings.
LoRaRadio.setCodingRate(LoRaRadio.CR_4_8);
LoRaRadio.setLnaBoost(true);

pinMode(SW1, INPUT);
pinMode(SW2, INPUT);
pinMode(32, INPUT);                         //Set inputs and outputs.

pinMode(RLED, OUTPUT);
pinMode(GLED, OUTPUT);

digitalWrite (RLED, LOW);
digitalWrite (GLED, LOW);

attachInterrupt(SW1, WakeyWakey, RISING);   //Attach an iterrupt flag to the two buttons.
attachInterrupt(SW2, WakeyWakey, RISING);
  

}

void loop() 
{
ButtonCheck();        //Checks for user button activity.
if(Wake_Flag == true)
{
  Wake_Flag = false;                          //Interrupt function to wake up from sleep on button press.
  attachInterrupt(SW1, WakeyWakey, RISING);
  attachInterrupt(SW2, WakeyWakey, RISING);
}

switch (Mode)         //Switch statement to determine what function to run based on the mode the cricket is in.
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

void AlarmMode()          //Function that is entered in to by a Bat module communicating with Cricket.                           
{                         //Cricket will sleep for 10 seconds then wake up, send its packet and go back to sleep.
  digitalWrite(GLED, HIGH);
  digitalWrite(RLED, HIGH);
  BuildPacket();
  digitalWrite(GLED, LOW);
  digitalWrite(RLED, LOW);
  delay(100);
  digitalWrite(GLED, HIGH);
  digitalWrite(RLED, HIGH);
  delay(100);
  digitalWrite(GLED, LOW);
  digitalWrite(RLED, LOW);
  delay(100);
  digitalWrite(GLED, HIGH);
  digitalWrite(RLED, HIGH);
  delay(100);
  digitalWrite(GLED, LOW);
  digitalWrite(RLED, LOW);
  STM32L0.stop(10000);
}

void BuildPacket()        //Function that builds the packet to be sent by the Cricket.
{
  char SendingPacket[4];
  SendingPacket[0] = '*';
  switch(DeviceID)                //Checks device ID being used and inputs the correct values in position 0 and 1 of our packet array.
  {
    case 0:
      SendingPacket[1] = '0';
      SendingPacket[2] = '0';
      break;
    case 1:
      SendingPacket[1] = '0';
      SendingPacket[2] = '1';
      break;
    case 2:
      SendingPacket[1] = '1';
      SendingPacket[2] = '0';
      break;
    case 3:
      SendingPacket[1] = '1';
      SendingPacket[2] = '1';
      break;
  }
  if(AlarmState == 1)              //Checks the status of the LimpState variable and appends the packet to indicate if its in this state or not.
  {
    SendingPacket[3] = '1';
  }
  else
  {
    SendingPacket[3] = '0';
  }
  if(DistressState == 1)          //Checks the status of the DistressState variable and appends the packet to indicate if its in this state or not.
  {
    SendingPacket[4] = '1';
  }
  else
  {
    SendingPacket[4] = '0';
  }
  
  SendPacket(SendingPacket);
}

void SendPacket(char SendingPacket[])         //Function that sends the built packet out through LoRa.
{
  LoRaRadio.beginPacket();
  for(int i = 0; i < 5; i++)
  {
    LoRaRadio.write(SendingPacket[i]);        //Sends each character individually of the packet array.
  }
  LoRaRadio.endPacket(true);
  delay(100);
  LoRaRadio.receive(1000); 
  LoRaRadio.parsePacket();     //Listens for a response for a Bat.
  if(LoRaRadio.read() == 'A' & AlarmState == 0)         //Changes to Alarm mode if it hears from a Bat.
  {
    Mode = Alarm;
    AlarmState = 1;
  }
}

void ButtonCheck()
{
  if(digitalRead(SW2) == 1)
  {
    SW2presstime = millis();
    aftertime = SW2presstime + 5000;
  }
  while(digitalRead(SW2) == 1)        //Checks if right button has been held down for 5 seconds then lights up red LED.
  {
    if(millis() > aftertime)
    {
      digitalWrite(RLED, HIGH);
      if(digitalRead(SW1) == 1)
      {
        count = count + 1;
        delay(500);
      }
      if(count == 3)
      {
        if(Mode != Alarm)
        {
          Mode = Distress;
          DistressState = true;       //If the left button is pressed 3 times while the right is still held down it will put the cricket in distress mode.
        }    
        count = 0;
      }
    } 
  }
  digitalWrite(RLED, LOW);
}

void WakeyWakey()                       //Button interrupt function.
{
  Wake_Flag = true;
  STM32L0.wakeup();
}
