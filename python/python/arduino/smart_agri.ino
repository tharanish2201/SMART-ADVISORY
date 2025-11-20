#include <SimpleDHT.h>

int pinDHT = 2;          // DHT11 DATA pin
SimpleDHT11 dht11;

int soilPin = A0;        // Soil moisture sensor

void setup() {
  Serial.begin(9600);
}

void loop() {
  byte temperature = 0;
  byte humidity = 0;

  // Read DHT11
  int err = dht11.read(pinDHT, &temperature, &humidity, NULL);
  if (err != SimpleDHTErrSuccess) {
    Serial.print("DHT11 read error: ");
    Serial.println(err);
    delay(2000);
    return;
  }

  // Read soil moisture (0-1023)
  int soil = analogRead(soilPin);

  // Convert to percentage (use the correct version)
  int soilPercent = map(soil, 1023, 0, 0, 100); // <--- use this if dry=1023, wet=0
  soilPercent = constrain(soilPercent, 0, 100);

  // Send values in CSV format to Python
  Serial.print((int)temperature);
  Serial.print(",");
  Serial.print((int)humidity);
  Serial.print(",");
  Serial.println(soilPercent);

  delay(3000);   // send data every 3 seconds
}
