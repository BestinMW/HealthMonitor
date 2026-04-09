import serial
import json
import paho.mqtt.client as mqtt

# -------------------------
# Serial setup (Arduino)
# -------------------------
ser = serial.Serial("COM3", 115200, timeout=1)  # Change to your port

# -------------------------
# MQTT setup
# -------------------------
broker = "34.136.195.75" #cloud vm ip thing
port = 8883
topic_publish = "sensor/vitals"
topic_subscribe = "results"
ca_cert_path = "ca.crt"      # Your CA certificate path

client = mqtt.Client()

# Use TLS with certificate verification
client.tls_set(ca_certs=ca_cert_path)

# -------------------------
# MQTT callbacks
# -------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(topic_subscribe)
    print(f"Subscribed to {topic_subscribe}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Received on {msg.topic}: {payload}")
    except Exception as e:
        print("Error processing message:", e)

client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
client.connect(broker, port)
client.loop_start()  # start network loop in background

# -------------------------
# Main loop: read Arduino, publish
# -------------------------
while True:
    line = ser.readline().decode().strip()
    if not line:
        continue

    try:
        data = json.loads(line)
        # ensure JSON has expected keys
        if all(k in data for k in ("hr", "spo2", "temp")):
            client.publish(topic_publish, line)
            print(f"Published to {topic_publish}: {line}")
        else:
            print("Missing keys in JSON:", line)
    except json.JSONDecodeError:
        print("Invalid JSON from Arduino:", line)