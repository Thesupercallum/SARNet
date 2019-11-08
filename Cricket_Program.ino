/*                Cricket Program
 *    This program is to be run on the Cricket device. It will have the 4 
 *    different modes that are able to be switched. Normal mode, Limp mode, 
 *    Alarm mode, and Distress mode.
 *    
 */




#include "LoRaRadio.h"
#include "STM32LowPower.h"

#define Address 2       //Address can be set to 0-4 for different Crickets.


#define Normal 0        //Define modes to be able to switch between them.
#define Distress 1
#define Alarm 2
#define Limp 3

int DistressState = 0;
int AlarmState = 0;
int LimpState = 1;


int DeviceID = Address;
int Mode = 0;

void setup() 
{
  Serial.begin(9600);
  LoRaRadio.begin(915000000);

  LoRaRadio.setFrequency(915000000);
  LoRaRadio.setTxPower(14);
  LoRaRadio.setBandwidth(LoRaRadio.BW_125);
  LoRaRadio.setSpreadingFactor(LoRaRadio.SF_7);
  LoRaRadio.setCodingRate(LoRaRadio.CR_4_5);
  LoRaRadio.setLnaBoost(true);
  

}

void loop() 
{
  LowPower.begin();
  ButtonCheck();
  delay(3000);
  /*
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
*/
}

void NormalMode ()        //Function that runs while in normal operation. Cricket will sleep for 5 minutes then wake and send out its packet and go back to sleep.
{
  Serial.print("Mode = Normal");
  //Green LED on
  BuildPacket();
  //Green LED off
  BatteryCheck();

  //sleep
}

void DistressMode ()      //Function that is entered in to by user of cricket to indicate trouble. 
{                         //Cricket will sleep for 1 minute then wake and send out its packet with distress indicator active and then go back to sleep.
  Serial.print("Mode = Distress");
  //Red LED on
  BuildPacket();
  //Red LED off
  BatteryCheck();
  
  //sleep
}

void AlarmMode()          //Function that is entered in to by a Bat module communicating with Cricket. Cricket will sleep for 10 seconds then wake up, send its packet and go back to sleep.
{
  Serial.print("Mode = Alarm");
  //Alternate between Green and Red LED going on
  BuildPacket();
  //LED goes off
  BatteryCheck();
  
  //sleep
}

void LimpMode()           //Function that is entered in to when the crickets battery liufe drops below a certain level. Cricket will sleep for 10 minutes then wake up, send its packet and go back to sleep.
{
  Serial.print("Mode = Limp");
  //Both LEDs come on
  BuildPacket();
  //Both LEDs go off
  BatteryCheck();

  //sleep
}

void BatteryCheck()       //Function that checks the battery level of the Cricket.
{
  
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
  if(LimpState == 1)              //Checks the status of the LimpState variable and appends the packet to indicate if its in this state or not.
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
  LoRaRadio.receive(1000);                                            //Listens for a response for a Bat.
  if(LoRaRadio.parsePacket() == 1 && LoRaRadio.read() == 'A')         //Changes to Alarm mode if it hears from a Bat.
  {
    Mode = Alarm;
  }
  else
  {
    
  }

  
}

void ButtonCheck()
{
  
}
