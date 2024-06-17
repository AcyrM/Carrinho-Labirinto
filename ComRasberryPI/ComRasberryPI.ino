#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <string.h>
#include <stdio.h>

BLEServer *pServer = NULL;
BLECharacteristic * pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint8_t txValue = 0;

int speed = 200;            // 255 = 46,12 cm/s;
std::string cmd;
int wait_time = 100, time_or_cmd, i;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
 
#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

#define pinMotor1_1 16     // PWM 1 - motor 1
#define pinMotor1_2 4      // PWM 2 - motor 1
#define pinMotor2_1 23     // PWM 1 - motor 2
#define pinMotor2_2 18    // PWM 2 - motor 2
#define pinMotor3_1 17   // PWM 2 - motor 2
#define pinMotor3_2 5    // PWM 2 - motor 2
#define pinMotor4_1 22    // PWM 2 - motor 2
#define pinMotor4_2 19

//--------------------------------CLASSES-------------------------------//
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };
 
    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};
 
class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      std::string rxValue = pCharacteristic->getValue();
      cmd = rxValue;
      if (rxValue.length() > 0) {
        Serial.print("CALLBACK Received Value: ");
        for (int i = 0; i < rxValue.length(); i++){
          Serial.print(cmd[i]);
        }
      }
    }
};

class DCMotor {  
  int spd = 255, pin1, pin2;
  int spdstop = 0;
  public:  
  
    void Pinout(int in1, int in2){ // Method for declaring motor pinout
      pin1 = in1;
      pin2 = in2;
      pinMode(pin1, OUTPUT);
      pinMode(pin2, OUTPUT);
      }       void Speed(int in1){ // Method for saving motor speed
      spd = in1;
      }     
    void Forward(){ // Method to go forward
      analogWrite(pin1, spd);
      digitalWrite(pin2, LOW);
      }   
    void Backward(){ // Method to go backward
      digitalWrite(pin1, LOW);
      analogWrite(pin2, spd);
      }
    void Stop(){ // Method to stop
      analogWrite(pin1, spdstop);
      analogWrite(pin2, spdstop);
      }
   };

DCMotor Motor1, Motor2, Motor3, Motor4;                 // Motor objects 

//------------------------------SETUP----------------------------//
void setup() {
  Serial.begin(9600);
  Motor1.Pinout(pinMotor1_1,pinMotor1_2); // Set motor pins.
  Motor2.Pinout(pinMotor2_1,pinMotor2_2); 
  Motor3.Pinout(pinMotor3_1,pinMotor3_2);
  Motor4.Pinout(pinMotor4_1,pinMotor4_2);

  // Create the BLE Device
  BLEDevice::init("UART Service For ESP32");
 
  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
 
  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);
 
  // Create a BLE Characteristic
  pTxCharacteristic = pService->createCharacteristic(
                                        CHARACTERISTIC_UUID_TX,
                                        BLECharacteristic::PROPERTY_NOTIFY
                                    );
                      
  pTxCharacteristic->addDescriptor(new BLE2902());
 
  BLECharacteristic * pRxCharacteristic = pService->createCharacteristic(
                                             CHARACTERISTIC_UUID_RX,
                                            BLECharacteristic::PROPERTY_WRITE
                                        );
 
  pRxCharacteristic->setCallbacks(new MyCallbacks());
 
  // Start the service
  pService->start();
 
  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("Waiting a client connection to notify...");
}
 
void loop() {
 
    if (deviceConnected) {
        if (cmd.length() > 0 && cmd != "CLEAR") {
          Serial.print("LOOP Received Value: ");
          for (int i = 0; i < cmd.length(); i++){
            Serial.print(cmd[i]);
            motor_control(cmd[i], speed, wait_time, Motor1, Motor2, Motor3, Motor4);
          }
          cmd = "CLEAR";
        }
        delay(10); // bluetooth stack will go into congestion, if too many packets are sent
    }
 
    // disconnecting
    if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("start advertising");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }
}

//------------------------------MOTORCONTROL---------------------------------//
void motor_control (char cmd, int speed,int del, DCMotor Motor1, DCMotor Motor2, DCMotor Motor3, DCMotor Motor4){
  if (cmd == 'F'){
    Motor1.Speed(speed); // Set motors speed
    Motor2.Speed(speed);
    Motor3.Speed(speed);
    Motor4.Speed(speed);
    Motor1.Forward(); 
    Motor2.Forward();
    Motor3.Forward();
    Motor4.Forward();
    Serial.print("FORWARD\n");
    delay(del);
  }
  else if (cmd == 'B'){
    Motor1.Speed(speed); // Set motors speed
    Motor2.Speed(speed);
    Motor3.Speed(speed);
    Motor4.Speed(speed);
    Motor1.Backward(); 
    Motor2.Backward();
    Motor3.Backward();
    Motor4.Backward();
    delay(del);
  }
  else if (cmd == 'R'){
    Motor1.Speed(speed); // Set motors speed
    Motor2.Speed(speed);
    Motor3.Speed(speed);
    Motor4.Speed(speed);
    Motor1.Forward(); 
    Motor2.Backward();
    Motor3.Backward();
    Motor4.Forward();
    delay(del);
  }
  else if (cmd == 'L'){
    Motor1.Speed(speed); // Set motors speed
    Motor2.Speed(speed);
    Motor3.Speed(speed);
    Motor4.Speed(speed);
    Motor1.Backward();
    Motor2.Forward();
    Motor3.Forward();
    Motor4.Backward();
    delay(del);
  }
  Serial.print("STOP\n");
  Motor1.Stop();
  Motor2.Stop();
  Motor3.Stop();
  Motor4.Stop();
}
