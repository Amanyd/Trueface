/*
  TrueFace Arduino Servo Control
  Controls servo motor based on face recognition results
  
  Hardware:
  - Servo connected to pin 9
  - Power: 5V and GND
  
  Communication:
  - Receives '1' → Move servo (face recognized)
  - Receives '0' → Return to original position (unknown face)
*/

#include <Servo.h>

Servo faceServo;  // Create servo object

const int servoPin = 9;
const int ledPin = 13;  // Built-in LED for status indication

// Servo positions
const int restPosition = 0;      // Default position
const int recognizedPosition = 90; // Position when face is recognized

void setup() {
  Serial.begin(9600);
  faceServo.attach(servoPin);
  pinMode(ledPin, OUTPUT);
  
  // Initialize servo to rest position
  faceServo.write(restPosition);
  digitalWrite(ledPin, LOW);
  
  Serial.println("TrueFace Arduino Ready!");
  Serial.println("Waiting for face recognition commands...");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case '1':
        // Face recognized - move servo and turn on LED
        faceServo.write(recognizedPosition);
        digitalWrite(ledPin, HIGH);
        Serial.println("Face recognized! Servo moved.");
        delay(1000);  // Hold position for 1 second
        break;
        
      case '0':
        // Unknown face or no face - return to rest position
        faceServo.write(restPosition);
        digitalWrite(ledPin, LOW);
        Serial.println("Unknown face. Servo returned to rest.");
        break;
        
      default:
        // Invalid command
        Serial.println("Invalid command. Use '1' for recognized, '0' for unknown.");
        break;
    }
  }
}
