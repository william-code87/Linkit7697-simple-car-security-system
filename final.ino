#include <LWiFi.h>
#include <LBLE.h>
#include <LBLEPeriphral.h>
#include <Servo.h>
#include <Ultrasonic.h>
#include <SPI.h>
#include <MFRC522.h>
#include "pitches.h"
#include "DHT.h"
char ssid[] = "WILLIAM 3152";    
char pass[] = "12345678";
int status = WL_IDLE_STATUS;
char server[] = "172.20.10.4"; 
WiFiClient client;
LBLEService AService("19B10010-E8F2-537E-4F6C-D104768A1214");
LBLECharacteristicString ARead("19B10011-E8F2-537E-4F6C-D104768A1214", LBLE_READ | LBLE_WRITE);
Servo myservo;
MFRC522 rfid(/*SS_PIN*/ 10, /*RST_PIN*/ 9);
String read_id;
String card_uid = "07ede7a4";
char c='d'; //d
int d=5; //1000
int flag=0; //0
int stopped=0;
char gas='0';
int temp;
int speeding;
Ultrasonic ultrasonic_2_3(4, 5); 

String mfrc522_readID()
{
  String ret;
  if ( rfid.PICC_IsNewCardPresent() &&rfid.PICC_ReadCardSerial())  //
   //讀取並確認不是重複卡片
  {
    MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
    for (byte i = 0; i < rfid.uid.size; i++) {
      ret += (rfid.uid.uidByte[i] < 0x10 ? "0" : "");
      ret += String(rfid.uid.uidByte[i], HEX);
    }//轉成16進制儲存
  }
 rfid.PICC_HaltA();
  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
  return ret;//回傳已完成轉存之id
}

void setup()
{
  // Initialize LED pin
  SPI.begin();
  rfid.PCD_Init();
  myservo.attach(3);
  Serial.begin(115200);
  LBLE.begin();
  while (!LBLE.ready()) { delay(100); }
  Serial.print("Device Address = [");
  Serial.print(LBLE.getDeviceAddress());
  Serial.println("]");
  
  LBLEAdvertisementData advertisement;
  advertisement.configAsConnectableDevice("D1072931");
  LBLEPeripheral.setName("D1072931");
  AService.addAttribute(ARead);
  LBLEPeripheral.addService(AService);
  LBLEPeripheral.begin();
  LBLEPeripheral.advertise(advertisement);
  while (!Serial) {
        ;
    }
}

void loop()
{
  while (status != WL_CONNECTED) {
       delay(3000);
       Serial.print("Attempting to connect to SSID: ");
       Serial.println(ssid);
       status = WiFi.begin(ssid, pass);
    }  
  if(gas=='0'){
    Serial.println("Connected to wifi");
    if (client.connect(server, 80)) {
        Serial.println("connected to server (GET)");
    }
  //  delay(1000);
    Serial.print("conected=");
    Serial.println(LBLEPeripheral.connected());
  }
  int current_angle=myservo.read();
  float distance = ultrasonic_2_3.convert(ultrasonic_2_3.timing(), Ultrasonic::CM);
  // Serial.print(distance);
//  delay(1000);
  while(!flag){
    Serial.println("locked"); 
    read_id = mfrc522_readID(); //呼叫函式取得16進制id
    if (read_id != "") {
      Serial.print("偵測到 RFID: ");
      Serial.println(read_id); 
      if(read_id==card_uid){
        flag=1;
      }
    }
  }
  else{
    Serial.println("unlocked");
    char value = ARead.getValue()[0];
    //Serial.println(value);
    if(value=='r')
      c='r';
    else if (value=='d')
      c='d';
    else if (value=='1')
      d=5;
    else if (value=='2')
      d=10;
    else if (value=='3')
      d=20;
    else if (value=='4')
      gas='4';
    else if (value=='0')
      gas='0';
    temp=d;
    if(c=='r'&&distance<=5){
      tone (6,NOTE_G5,300);
      stopped=1;
      String GET="GET /insert1.php";
      String getStr = GET + "?d="+ distance +
              " HTTP/1.1";
      client.println(getStr);
      client.println("Host: 172.20.10.4");
      client.println("Accept: */*");
      client.println("Connection: close");
      client.println();
    }
    else if(c=='r'&&distance<=50){
      d=5;
      stopped=0;
      tone (6,NOTE_G5,100);
      String GET="GET /insert1.php";
      String getStr = GET + "?d="+ distance +
              " HTTP/1.1";
      client.println(getStr);
      client.println("Host: 172.20.10.4");
      client.println("Accept: */*");
      client.println("Connection: close");
      client.println();
    }
    else if(c=='d'||distance>50){
      stopped=0;
      d=temp;
    }
    //Serial.print((int)d);
    //Serial.print((int)stopped);
    switch (gas) {
      case '4':
        if(!stopped){
          if(c=='r')
          {
            if(current_angle>=150)
            {
              tone (6,NOTE_C5,300);
              myservo.write(0);
            }
            else
            {
              current_angle+=d;
              myservo.write(current_angle);//將角度寫入馬達
            }
          }
          else if(c=='d')
          {
            if(current_angle<=6)
            {
              tone (6,NOTE_C6,300);
              myservo.write(180);
            }
            else
            {
              current_angle-=d;
              myservo.write(current_angle);//將角度寫入馬達
            }
          }
          //Serial.println("ON");
        }
        break;
      case '0':
        //Serial.println("OFF");
        break;
      default:
        //Serial.println("Unknown value written");
        break;
    if(d==1000)
      speeding=1;
    else if(d==500)
      speeding=2;
    else
      speeding=3;
    String text = "distance:" + distance + "," + "speed:" + speeding + ",";
    Serial.println(text);
    }
  }
}
