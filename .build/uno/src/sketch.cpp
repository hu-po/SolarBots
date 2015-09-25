#include <Arduino.h>
#include <NewPing.h>
#include <TSL2561.h>
void setup();
void loop();
void echoCheck();
void sonarSensorCycle();
void lumSensorCycle();
#line 1 "src/sketch.pde"
// ---------------------------------------------------------------------------
// This example code was used to successfully communicate with 15 ultrasonic sensors. You can adjust
// the number of sensors in your project by changing SONAR_NUM and the number of NewPing objects in the
// "sonar" array. You also need to change the pins for each sensor for the NewPing objects. Each sensor
// is pinged at 33ms intervals. So, one cycle of all sensors takes 495ms (33 * 15 = 495ms). The results
// are sent to the "oneSensorCycle" function which currently just displays the distance data. Your project
// would normally process the sensor results in this function (for example, decide if a robot needs to
// turn and call the turn function). Keep in mind this example is event-driven. Your complete sketch needs
// to be written so there's no "delay" commands and the loop() cycles at faster than a 33ms rate. If other
// processes take longer than 33ms, you'll need to increase PING_INTERVAL so it doesn't get behind.
// ---------------------------------------------------------------------------
//#include <NewPing.h>
//#include <TSL2561.h>

#define SONAR_NUM     3 // Number or sensors.
#define MAX_DISTANCE 100 // Maximum distance (in cm) to ping.
#define PING_INTERVAL 40 //33 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).

unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
unsigned int cm[SONAR_NUM];         // Where the ping distances are stored.
uint8_t currentSensor = 0;          // Keeps track of which sensor is active.

TSL2561 tsl_1(TSL2561_ADDR_FLOAT);
TSL2561 tsl_2(TSL2561_ADDR_LOW);
TSL2561 tsl_3(TSL2561_ADDR_HIGH);

NewPing sonar[SONAR_NUM] = {     // Sensor object array.
  NewPing(12, 13, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
  NewPing(8, 9, MAX_DISTANCE),
  NewPing(10, 11, MAX_DISTANCE),
};

void setup() {
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

  pingTimer[0] = millis() + 75;           // First ping starts at 75ms, gives time for the Arduino to chill before starting.
  for (uint8_t i = 1; i < SONAR_NUM; i++) // Set the starting time for each sensor.
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
}

void loop() {
  for (uint8_t i = 0; i < SONAR_NUM; i++) { // Loop through all the sensors.
    if (millis() >= pingTimer[i]) {         // Is it this sensor's time to ping?
      pingTimer[i] += PING_INTERVAL * SONAR_NUM;  // Set next time this sensor will be pinged.
      if (i == 0 && currentSensor == SONAR_NUM - 1) sonarSensorCycle(); // Sensor ping cycle complete, do something with the results.
      sonar[currentSensor].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
      currentSensor = i;                          // Sensor being accessed.
      cm[currentSensor] = 0;                      // Make distance zero in case there's no ping echo for this sensor.
//      sonar[currentSensor].ping_median(3);			// Multiple pings and return median
      sonar[currentSensor].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
    }
  }
 sonarSensorCycle();
 lumSensorCycle();
}

void echoCheck() { // If ping received, set the sensor distance to array.
  if (sonar[currentSensor].check_timer())
  cm[currentSensor] = sonar[currentSensor].ping_median(3) / US_ROUNDTRIP_CM;   
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}

void sonarSensorCycle() { // Sensor ping cycle complete, do something with the results.
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    Serial.print(i);
    Serial.print("=");
    Serial.print(cm[i]);
    Serial.print(",");
    Serial.print("cm ");
  }
 Serial.println();
}

void lumSensorCycle() {
 uint16_t x_1 = tsl_1.getLuminosity(TSL2561_INFRARED);
 uint16_t x_2 = tsl_2.getLuminosity(TSL2561_INFRARED);
 uint16_t x_3 = tsl_3.getLuminosity(TSL2561_INFRARED);

 Serial.print("Measuring ... \(");
 Serial.print(x_1, DEC); Serial.print(",");
 Serial.print(x_2, DEC); Serial.print(",");
 Serial.println(x_3, DEC);// Serial.print(")");
 Serial.println("... done");

}

