#include <Wire.h>
#include <math.h>
#include <Servo.h>
#include "TSL2561.h"

// Arduino pins for the shift register
#define MOTORLATCH 12
#define MOTORCLK 4
#define MOTORENABLE 7
#define MOTORDATA 8

// 8-bit bus after the 74HC595 shift register 
// (not Arduino pins)
// These are used to set the direction of the bridge driver.
#define MOTOR1_A 2
#define MOTOR1_B 3
#define MOTOR2_A 1
#define MOTOR2_B 4

// Arduino pins for the PWM signals.
#define MOTOR1_PWM 11
#define MOTOR2_PWM 3

// Codes for the motor function.
#define FORWARD 1
#define BACKWARD 2
#define BRAKE 3
#define RELEASE 4

TSL2561 tsl_1(TSL2561_ADDR_FLOAT); 
TSL2561 tsl_2(TSL2561_ADDR_LOW);
TSL2561 tsl_3(TSL2561_ADDR_HIGH);

int lum_hist_1[6];
int lum_hist_2[6];
int lum_hist_3[6];

int seconds_per_rotate = 6000; //Time to rotate 360 degrees
int seconds_per_move = 1200; //Time to move 5 cm
int motor_power = 108; //motor power to use, changes with floor

int threshold = 1000; //Threshold for high light

// Direction unit vectors for the three sensors
float sensor_1_vector[2] = {1.0, 0};
float sensor_2_vector[2] = {-0.5, -0.88}; //needs to point a bit backwards or else robot will only ever move forward
float sensor_3_vector[2] = {-0.5, 0.88};



void setup(void) {
  Serial.begin(9600);
  
  if (tsl_1.begin()) {
    Serial.println("Found Sensor 1 (Float)");
  } else {
    Serial.println("Sensor 1 Load Failure");
    while (1);
  }

  if (tsl_2.begin()) {
    Serial.println("Found Sensor 2 (Low)");
  } else {
    Serial.println("Sensor 2 Load Failure");
    while (1);
  }

  if (tsl_3.begin()) {
    Serial.println("Found Sensor 3 (High)");
  } else {
    Serial.println("Sensor 3 Load Failure");
    while (1);
  }

  Serial.print("Setting Gain ...");
  tsl_1.setGain(TSL2561_GAIN_16X); // low light gain
  tsl_2.setGain(TSL2561_GAIN_16X);
  tsl_3.setGain(TSL2561_GAIN_16X);
  Serial.println("done");
  
  Serial.print("Setting Integration Time ...");
  tsl_1.setTiming(TSL2561_INTEGRATIONTIME_13MS);  // medium light
  tsl_2.setTiming(TSL2561_INTEGRATIONTIME_13MS);
  tsl_3.setTiming(TSL2561_INTEGRATIONTIME_13MS);
  Serial.println("done");

}

void loop(void) {
  
 for(byte k = 3; k>0; k--)
 {
    
   Serial.print("Measuring ... \(");
   uint16_t x_1 = tsl_1.getLuminosity(TSL2561_INFRARED);
   uint16_t x_2 = tsl_2.getLuminosity(TSL2561_INFRARED);
   uint16_t x_3 = tsl_3.getLuminosity(TSL2561_INFRARED);
  
   Serial.print(x_1, DEC); Serial.print(",");
   Serial.print(x_2, DEC); Serial.print(",");
   Serial.print(x_3, DEC); Serial.print(")");
   Serial.println("... done");

  // Shift data in history array
  for(byte i=3; i>0; i--)
  {
    lum_hist_1[i] = lum_hist_1[i-1];
    lum_hist_2[i] = lum_hist_2[i-1];
    lum_hist_3[i] = lum_hist_3[i-1];
  }

  // Write new data to the front of the array
  lum_hist_1[0] = x_1;
  lum_hist_2[0] = x_2;
  lum_hist_3[0] = x_3;

  Serial.print("Waiting for next measure ...");
  Serial.print(k);
  delay(500);
  Serial.println("done");
}

  // Determine average luminosity for each sensor
  float avg_1 = (float)(lum_hist_1[2] + lum_hist_1[1] + lum_hist_1[0]) / 3.0;
  float avg_2 = (float)(lum_hist_2[2] + lum_hist_2[1] + lum_hist_2[0]) / 3.0;
  float avg_3 = (float)(lum_hist_3[2] + lum_hist_3[1] + lum_hist_3[0]) / 3.0;

  // Display array  
  Serial.print("Sensor 1: [");
  for(byte i=3; i > 0; i--)
  {
    Serial.print(lum_hist_1[i-1]);
    Serial.print(",");
  }
  Serial.print("] -> avg: ");
  Serial.println(avg_1); 

  Serial.print("Sensor 2: [");
  for(byte i=3; i > 0; i--)
  {
    Serial.print(lum_hist_2[i-1]);
    Serial.print(",");
  }
  Serial.println("] -> avg: ");
  Serial.println(avg_2); 

  Serial.print("Sensor 3: [");
  for(byte i=3; i > 0; i--)
  {
    Serial.print(lum_hist_3[i-1]);
    Serial.print(",");
  }
  Serial.println("] -> avg: ");
  Serial.println(avg_3);

if(avg_1 > threshold || (avg_1 > avg_2 && avg_1 > avg_3))
{ 
	float vector[2] = sensor_1_vector;
	Serial.println("Towards Sensor 1");
}

else if(avg_2 > threshold || (avg_2 > avg_1 && avg_2 > avg_3))
{
	float vector[2] = sensor_2_vector;
	Serial.println("Towards Sensor 2");
}

else if(avg_3 > threshold || (avg_3 > avg_2 && avg_3 > avg_1))
{
	float vector[2] = sensor_3_vector;
	Serial.println("Towards Sensor 3");
}

else
{
	float vector[2] = {1,0};
	Serial.println("PlantBot is confused");
}

  delay(5000);

  move(vector);

  delay(10000); 
}

void move(float vector[])
{
 //Plan movement based on vector direction

 //Determine angle using atan2()
    float rot_angle = atan2(vector[0], vector[1]);
    //float rot_angle = 3.1415; //TEST CASE
	
    Serial.print("rot_angle: "); Serial.println(rot_angle);


 // Rotate
    float rot_time = abs((rot_angle/3.14) * seconds_per_rotate);
    
    Serial.print("rot_time: "); Serial.println(rot_time);

    if(rot_angle > 0) //Rotate to the RIGHT
    {
	Serial.println("Rotate RIGHT");
	motor(1, BACKWARD, motor_power);
	motor(2, FORWARD, motor_power);
	delay((int)rot_time);
    }
    else //Rotate to the LEFT
    {
	Serial.println("Rotate LEFT");
	motor(1, FORWARD, motor_power);
	motor(2, BACKWARD, motor_power);
	delay((int)rot_time);
    }
    motor(1, RELEASE, 0);
    motor(2, RELEASE, 0);
    delay(500);

 // Move
   
Serial.print("seconds_per_move: "); Serial.println(dist_time);

    motor(1, FORWARD, motor_power);
    motor(2, FORWARD, motor_power);
    delay(seconds_per_move);
    motor(1, RELEASE, 0);
    motor(2, RELEASE, 0);
    delay(500);

}

// ---------------------------------
// motor
//
// Select the motor (1-4), the command, 
// and the speed (0-255).
// The commands are: FORWARD, BACKWARD, BRAKE, RELEASE.
//
void motor(int nMotor, int command, int speed)
{
  int motorA, motorB;

  if (nMotor >= 1 && nMotor <= 4)
  {  
    switch (nMotor)
    {
    case 1:
      motorA   = MOTOR1_A;
      motorB   = MOTOR1_B;
      break;
    case 2:
      motorA   = MOTOR2_A;
      motorB   = MOTOR2_B;
      break;
    default:
      break;
    }

    switch (command)
    {
    case FORWARD:
      motor_output (motorA, HIGH, speed);
      motor_output (motorB, LOW, -1);     // -1: no PWM set
      break;
    case BACKWARD:
      motor_output (motorA, LOW, speed);
      motor_output (motorB, HIGH, -1);    // -1: no PWM set
      break;
    case BRAKE:
      // The AdaFruit library didn't implement a brake.
      // The L293D motor driver ic doesn't have a good
      // brake anyway.
      // It uses transistors inside, and not mosfets.
      // Some use a software break, by using a short
      // reverse voltage.
      // This brake will try to brake, by enabling 
      // the output and by pulling both outputs to ground.
      // But it isn't a good break.
      motor_output (motorA, LOW, 255); // 255: fully on.
      motor_output (motorB, LOW, -1);  // -1: no PWM set
      break;
    case RELEASE:
      motor_output (motorA, LOW, 0);  // 0: output floating.
      motor_output (motorB, LOW, -1); // -1: no PWM set
      break;
    default:
      break;
    }
  }
}


// ---------------------------------
// motor_output
//
// The function motor_ouput uses the motor driver to
// drive normal outputs like lights, relays, solenoids, 
// DC motors (but not in reverse).
//
// It is also used as an internal helper function 
// for the motor() function.
//
// The high_low variable should be set 'HIGH' 
// to drive lights, etc.
// It can be set 'LOW', to switch it off, 
// but also a 'speed' of 0 will switch it off.
//
// The 'speed' sets the PWM for 0...255, and is for 
// both pins of the motor output.
//   For example, if motor 3 side 'A' is used to for a
//   dimmed light at 50% (speed is 128), also the 
//   motor 3 side 'B' output will be dimmed for 50%.
// Set to 0 for completelty off (high impedance).
// Set to 255 for fully on.
// Special settings for the PWM speed:
//    Set to -1 for not setting the PWM at all.
//
void motor_output (int output, int high_low, int speed)
{
  int motorPWM;

  switch (output)
  {
  case MOTOR1_A:
  case MOTOR1_B:
    motorPWM = MOTOR1_PWM;
    break;
  case MOTOR2_A:
  case MOTOR2_B:
    motorPWM = MOTOR2_PWM;
    break;
  default:
    // Use speed as error flag, -3333 = invalid output.
    speed = -3333;
    break;
  }

  if (speed != -3333)
  {
    // Set the direction with the shift register 
    // on the MotorShield, even if the speed = -1.
    // In that case the direction will be set, but
    // not the PWM.
    shiftWrite(output, high_low);

    // set PWM only if it is valid
    if (speed >= 0 && speed <= 255)    
    {
      analogWrite(motorPWM, speed);
    }
  }
}


// ---------------------------------
// shiftWrite
//
// The parameters are just like digitalWrite().
//
// The output is the pin 0...7 (the pin behind 
// the shift register).
// The second parameter is HIGH or LOW.
//
// There is no initialization function.
// Initialization is automatically done at the first
// time it is used.
//
void shiftWrite(int output, int high_low)
{
  static int latch_copy;
  static int shift_register_initialized = false;

  // Do the initialization on the fly, 
  // at the first time it is used.
  if (!shift_register_initialized)
  {
    // Set pins for shift register to output
    pinMode(MOTORLATCH, OUTPUT);
    pinMode(MOTORENABLE, OUTPUT);
    pinMode(MOTORDATA, OUTPUT);
    pinMode(MOTORCLK, OUTPUT);

    // Set pins for shift register to default value (low);
    digitalWrite(MOTORDATA, LOW);
    digitalWrite(MOTORLATCH, LOW);
    digitalWrite(MOTORCLK, LOW);
    // Enable the shift register, set Enable pin Low.
    digitalWrite(MOTORENABLE, LOW);

    // start with all outputs (of the shift register) low
    latch_copy = 0;

    shift_register_initialized = true;
  }

  // The defines HIGH and LOW are 1 and 0.
  // So this is valid.
  bitWrite(latch_copy, output, high_low);

  // Use the default Arduino 'shiftOut()' function to
  // shift the bits with the MOTORCLK as clock pulse.
  // The 74HC595 shiftregister wants the MSB first.
  // After that, generate a latch pulse with MOTORLATCH.
  shiftOut(MOTORDATA, MOTORCLK, MSBFIRST, latch_copy);
  delayMicroseconds(5);    // For safety, not really needed.
  digitalWrite(MOTORLATCH, HIGH);
  delayMicroseconds(5);    // For safety, not really needed.
  digitalWrite(MOTORLATCH, LOW);
}


