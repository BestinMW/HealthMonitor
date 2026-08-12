# HealthMonitor

## Description
This device belongs to the consumer healthcare and remote health monitoring industry. The goal is to provide individuals with a convenient, at-home tool for monitoring basic health indicators so they can better assess whether medical attention is necessary.

Many people struggle to determine whether symptoms such as feeling unwell, fatigued, or light-headed are minor or require a hospital visit. Hospital visits can be inconvenient, time-consuming, and expensive, especially when symptoms turn out to be non-critical. Our device focuses on monitoring three key vital signs: body temperature, heart rate, and blood oxygen saturation (SpO₂). Regular monitoring of these vitals allows users to establish a personal baseline and detect irregularities over time.

By identifying abnormal readings early, users can make more informed decisions about seeking professional medical care. While the device is not intended to replace a medical professional, it can help reduce unnecessary hospital visits and promote proactive health awareness.

Foreseen challenges include ensuring sensor accuracy, handling noisy or inconsistent data, protecting sensitive health information, and clearly communicating results without causing unnecessary alarm or providing misleading medical claims.

## Solution
Our full-scale solution is an all-in-one smart health monitoring device capable of measuring key vital signs such as body temperature, heart rate, and blood oxygen levels. The collected data is analyzed using AI-based algorithms to identify abnormal patterns or trends.

Instead of providing a definitive medical diagnosis, the system generates health insights and risk indicators (e.g., “possible fever,” “elevated heart rate,” or “low blood oxygen level”) along with recommendations such as monitoring symptoms, resting, or consulting a healthcare professional. The device presents results in a clear, user-friendly report that is easy to understand for non-technical users.


## Network Diagram
<img width="253" height="512" alt="unnamed (2) (1)" src="https://github.com/user-attachments/assets/77411f4f-9bfd-435f-b429-ca5e81ff0dd6" />


## Device Catalog
### Arduino Uno R3
ATmega328P microcontroller
14 digital I/O pins (6 PWM)
6 analog input pins
USB interface for programming and serial communication
Supports I2C, SPI, and UART communication
- Role:
Reads data and processes signals, transmits health data to Laptop
### MAX30102 Sensor
Measures Heart Rate
Measures SpO₂
I2C communication
Infrared + Red LED photoplethysmography
- Role:
Real-time HR and oxygen saturation measurement
### SEN0206 Temperature Sensor
High precision temperature sensor
I2C Wire Protocol
- Role:
Body temperature monitoring

## Network Operation
### Services:
Google Cloud Compute Engine
Uses a virtual machine to host MQTT broker
Runs the trained ML model on received message from MQTT
Returns result through MQTT publish to result topic
Mosquitto MQTT Broker
pub/sub system in between edge and cloud
Broker is run on the Jetson and Cloud VM
Encrypts information through TLS
Quality Attributes:
Security: Information between the edge layer and cloud layer is mainly upheld by MQTT through TLS encryption. Google Cloud also includes VPC firewall restrictions for added protection.
Privacy: No information is stored, only takes sensor input and returns the results of those inputs. Our AI model is pretrained on a synthetic patient dataset and won’t collect user information.
Reliability: Ability to fallback on edge layer for computation when cloud service is unavailable.
Messaging & Communication Protocols:
Pub/Sub Messaging (MQTT)
Reliant on events (publishing to topics)
Ran in Jetson Nano
Publishes vital data
Subscribes for result data
Ran in Google Cloud Run
Subscribes for vital data
Publishes result data
MQTT Communication Protocols:
TLS: encrypts data and provides added security through certification authentication.
TCP: allows for information to reliably reach the edge and cloud layers.
QoS level 1: At least once protocol that also allows for reliable information transfer as information is received and acknowledged “at least once.”

## Existing Products Comparison
<img width="512" height="196" alt="unnamed (3)" src="https://github.com/user-attachments/assets/827b4791-815b-40f7-826c-92753a7b1162" />
The chart above shows how our device price compares to the Apple Watch Series 11, Fitbit Charge 6, and Oura Ring 4. Our device costs approximately $45 in hardware, which is roughly 9x cheaper than the Apple Watch Series 11 and 8x cheaper than the Oura Ring 4. While consumer devices offer polished form factors and ecosystem integrations, they do not provide on-demand AI risk classification from raw vitals. Our device fills this gap at a fraction of the cost, making it accessible as a research or proof-of-concept platform.
Future Improvements
- Create housing that allows for easier usage of the device
- Add additional sensors to collect more vitals (Blood pressure, fall detection)
- Store separate user data for more personalized predictions
- Add Individual user profiles
- Use real data rather than synthetic data to train the model
