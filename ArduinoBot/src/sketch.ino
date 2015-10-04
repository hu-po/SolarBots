#include <NewPing.h>
#include <TSL2561.h>

#define SONAR_NUM     4 // Number or sensors.
#define MAX_DISTANCE  100 // Maximum distance (in cm) to ping.
#define PING_INTERVAL  40 //33 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).

unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
unsigned int cm[SONAR_NUM];         // Where the ping distances are stored.
uint8_t currentSensor = 0;          // Keeps track of which sensor is active.

TSL2561 tsl_1(TSL2561_ADDR_HIGH);
TSL2561 tsl_2(TSL2561_ADDR_LOW);
TSL2561 tsl_3(TSL2561_ADDR_FLOAT);

NewPing sonar[SONAR_NUM] = {     // Sensor object array.
  NewPing(14, 15, MAX_DISTANCE),
  NewPing(8, 9, MAX_DISTANCE),
  NewPing(10, 11, MAX_DISTANCE),
  NewPing(12, 13, MAX_DISTANCE) // Each sensor's trigger pin, echo pin, and max distance to ping.
};

void setup() {

  Serial.begin(9600);

  tsl_1.begin();
  tsl_2.begin();
  tsl_3.begin();

  tsl_1.setGain(TSL2561_GAIN_16X); // low light gain
  tsl_2.setGain(TSL2561_GAIN_16X);
  tsl_3.setGain(TSL2561_GAIN_16X);

  tsl_1.setTiming(TSL2561_INTEGRATIONTIME_13MS);  // medium light
  tsl_2.setTiming(TSL2561_INTEGRATIONTIME_13MS);
  tsl_3.setTiming(TSL2561_INTEGRATIONTIME_13MS);

  pingTimer[0] = millis() + 75;           // First ping starts at 75ms, gives time for the Arduino to chill before starting.
  for (uint8_t i = 1; i < SONAR_NUM; i++) // Set the starting time for each sensor.
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
}

void loop() {
  for (uint8_t i = 0; i < SONAR_NUM; i++) {                // Loop through all the sensors.
      if (millis() >= pingTimer[i]) {                                   // Is it this sensor's time to ping?
      pingTimer[i] += PING_INTERVAL * SONAR_NUM; // Set next time this sensor will be pinged.
      if (i == 0 && currentSensor == SONAR_NUM - 1) // Sensor ping cycle complete, do something with the results.
        SensorCycle(); // Do something with results.
      sonar[currentSensor].timer_stop();                        // Make sure previous timer is canceled before starting a new ping (insurance).
      currentSensor = i;                                                  // Sensor being accessed.
      cm[currentSensor] = 0;                                         // Make distance zero in case there's no ping echo for this sensor.
      sonar[currentSensor].ping_timer(echoCheck);     // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
    }
  }
}

void echoCheck() { // If ping received, set the sensor distance to array.
  if (sonar[currentSensor].check_timer())
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}

void SensorCycle() { // Sensor ping cycle complete, do something with the results.

  for (uint8_t i = 1; i < SONAR_NUM; i++) {
    Serial.print(cm[i]);
    Serial.print(",");
  }

// Print out TSL2561 readings as well
Serial.print(tsl_1.getLuminosity(TSL2561_INFRARED)); Serial.print(",");
Serial.print(tsl_2.getLuminosity(TSL2561_INFRARED)); Serial.print(",");
Serial.print(tsl_3.getLuminosity(TSL2561_INFRARED));

Serial.println();  // New line to indicate end of sensing cycle

}

