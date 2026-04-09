#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <DFRobot_MLX90614.h>
#define BUFFER_SIZE 50

uint16_t irBuffer[BUFFER_SIZE];
uint16_t redBuffer[BUFFER_SIZE];
int bufferIndex = 0;

float spo2;

float calculateSpO2() {
  // Calculate DC (average)
  long irSum = 0;
  long redSum = 0;
  for (int i = 0; i < BUFFER_SIZE; i++) {
    irSum += irBuffer[i];
    redSum += redBuffer[i];
  }
  float irDC = irSum / (float)BUFFER_SIZE;
  float redDC = redSum / (float)BUFFER_SIZE;

  // Calculate AC (peak-to-peak)
  uint16_t irMax = irBuffer[0], irMin = irBuffer[0];
  uint16_t redMax = redBuffer[0], redMin = redBuffer[0];
  for (int i = 0; i < BUFFER_SIZE; i++) {
    if (irBuffer[i] > irMax) irMax = irBuffer[i];
    if (irBuffer[i] < irMin) irMin = irBuffer[i];
    if (redBuffer[i] > redMax) redMax = redBuffer[i];
    if (redBuffer[i] < redMin) redMin = redBuffer[i];
  }
  float irAC = irMax - irMin;
  float redAC = redMax - redMin;

  // Avoid divide by zero
  if (irAC == 0 || irDC == 0 || redDC == 0) return -1;

  float R = (redAC / redDC) / (irAC / irDC);

  // Empirical formula
  float SpO2 = 110.0 - 25.0 * R;

  // Clamp values
  if (SpO2 > 100) SpO2 = 100;
  if (SpO2 < 0) SpO2 = 0;

  return SpO2;
}

DFRobot_MLX90614_I2C sensor;

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute = 0;
int beatAvg = 0;
int count = 0;

unsigned long lastPrint = 0;
const unsigned long printInterval = 500;  // milliseconds

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing...");

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 was not found. Please check wiring/power.");
    while (1)
      ;
  }

  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);

  while (NO_ERR != sensor.begin()) {
    Serial.println("Communication with device failed, please check connection");
    delay(3000);
  }
  Serial.println("Begin ok!");

  sensor.enterSleepMode();
  delay(50);
  sensor.enterSleepMode(false);
  delay(200);
}

void loop() {
  uint16_t irValue = particleSensor.getIR();
  uint16_t redValue = particleSensor.getRed();

  // store readings in circular buffer
  irBuffer[bufferIndex] = irValue;
  redBuffer[bufferIndex] = redValue;
  bufferIndex = (bufferIndex + 1) % BUFFER_SIZE;

  if (checkForBeat(irValue)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;

      beatAvg = 0;
      for (byte x = 0; x < RATE_SIZE; x++) beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }

  if (millis() - lastPrint > printInterval) {
    lastPrint = millis();

    if (irValue < 5000) {
      // Serial.println("No finger detected");
      spo2 = 0;
      beatsPerMinute = 0;
      beatAvg = 0;
    } else {
      // calculate SpO2 when buffer is full
      spo2 = calculateSpO2();
    }

    float ambientTemp = sensor.getAmbientTempCelsius();
    float objectTemp = sensor.getObjectTempCelsius();

    Serial.print(beatAvg);
    Serial.print(",");
    Serial.print(spo2);
    Serial.print(",");
    Serial.print(objectTemp);
    Serial.println();
  }
}