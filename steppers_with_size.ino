/* Program for recieving serial input to control stepper motors */

// Include the AccelStepper library:
#include <AccelStepper.h>

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPinX 11
#define stepPinX 10

#define dirPinY 13
#define stepPinY 12

#define dirPinZ 9
#define stepPinZ 8

#define motorInterfaceType 1

// Create new instances of the AccelStepper class:
AccelStepper stepperX = AccelStepper(motorInterfaceType, stepPinX, dirPinX);
AccelStepper stepperY = AccelStepper(motorInterfaceType, stepPinY, dirPinY);
AccelStepper stepperZ = AccelStepper(motorInterfaceType, stepPinZ, dirPinZ);

// Declare required variables
char receivedChar;
int speed = 500;
int Zspeed = 400;

void setup() {
  // Set the maximum speed in steps per second:
  pinMode (A4, OUTPUT);
  digitalWrite(A4,LOW);
  pinMode (A5, OUTPUT);
  digitalWrite(A5,LOW);
  stepperX.setMaxSpeed(800);
  stepperY.setMaxSpeed(800);
  stepperZ.setMaxSpeed(600);
  //Starts serial interface with given baudrate (must match sender rate)
  Serial.begin(57600);
  Serial.println("<Arduino is ready>");
}

void loop() {
  recvOneChar();

  // Controls stepper motors based on recieved character from serial
  if (receivedChar == 's'){
    stepperY.setSpeed(-speed);
    stepperY.runSpeed();
 }
  if (receivedChar == 'w'){
    stepperY.setSpeed(speed);
    stepperY.runSpeed();
 }
 if (receivedChar == 'a'){
    stepperX.setSpeed(-speed);
    stepperX.runSpeed();
 }
 if (receivedChar == 'd'){
    stepperX.setSpeed(speed);
    stepperX.runSpeed();
 }
  if (receivedChar == 'o'){
    stepperZ.setSpeed(Zspeed);
    stepperZ.runSpeed();
 }
  if (receivedChar == 'l'){
    stepperZ.setSpeed(-Zspeed);
    stepperZ.runSpeed();
 }
 if (receivedChar == 'e'){
    stepperX.setSpeed(speed);
    stepperY.setSpeed(speed);
    stepperX.runSpeed();
    stepperY.runSpeed();
 }

 if (receivedChar == 'q'){
    stepperX.setSpeed(-speed);
    stepperY.setSpeed(speed);
    stepperX.runSpeed();
    stepperY.runSpeed();
 }

 if (receivedChar == 'z'){
    stepperX.setSpeed(-speed);
    stepperY.setSpeed(-speed);
    stepperX.runSpeed();
    stepperY.runSpeed();
 }

 if (receivedChar == 'c'){
    stepperX.setSpeed(speed);
    stepperY.setSpeed(-speed);
    stepperX.runSpeed();
    stepperY.runSpeed();
 }

 if (receivedChar == '1'){
    digitalWrite(A4,HIGH);
    digitalWrite(A5,LOW);
 }

  if (receivedChar == '2'){
    digitalWrite(A4,LOW);
    digitalWrite(A5,LOW);
 }

  if (receivedChar == '3'){
    digitalWrite(A4,HIGH);
    digitalWrite(A5,HIGH);
 }

//Makes sure the motor speed stays within reasonable limits
// Test adding delay for better control of speed here
if (receivedChar == 'r'){
  if (speed < 1000){
    speed = speed + 1;
  }
}
if (receivedChar == 'f'){
  if (speed >500){
    speed = speed -1;
  }
}
}

//Recieves characters from serial port and stores them in variable
void recvOneChar() {
 if (Serial.available() > 0) {
 receivedChar = Serial.read();
 }
}