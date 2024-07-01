void setup() {
    Serial.begin(9600); // Initialize USB serial communication for debugging
    Serial1.begin(9600); // Initialize hardware UART on default pins (TX: D9, RX: D10)
    Serial.println("UART initialized");
}

void loop() {
    if (Serial1.available()) {
        float data_received = Serial1.parseFloat(); // The data from UART is saved onto data_received. Rename "data_received" to what you'd like
        Serial.print("Received data: "); 
        Serial.println(data_received, 2); // Print the data received to the Serial monitor for easier debugging
        Serial.print("\n"); // Creates a new line :)
        delay(10); // 10 millisecond 
        Particle.connected(); // Up to the if statement checks the connection then will upload it to events 
        SerialLogHandler logHandler;
        if (Particle.connected()) {
            Log.info("Connected!"); // This will be printed in events tab 
                Particle.publish("Phototransistor value"/*Change this to your corresponding sensor*/, String::format("%.2f",data_received), NULL, NO_ACK); 
                // Line directly above is posting the value from the feather m4 onto the events tab 

        }else{
            Serial.print("Device not connected");
        }

    } else {
        Serial.println("Data not received."); /* Will print if you aren't sending any data to the board.
        Check your connections make sure RX on the particle board is connected to TX on the feather and vice versa*/
        delay(1000); 
    }
}

