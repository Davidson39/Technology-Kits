import time
import board
import analogio
import busio
import digitalio

# phototransistor connected to A1
phototransistor = analogio.AnalogIn(board.A1)
# LED connected to D1
led = digitalio.DigitalInOut(board.D1)
led.direction = digitalio.Direction.OUTPUT
# Initializing UART
uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=1)

def get_voltage(pin):
    return float((pin.value * 3.3) / 65536)

def control_led(voltage, threshold=0.3):
    if voltage > threshold:  # Turn on the LED if voltage is above threshold
        led.value = True
    else:  # Turn off the LED if voltage is below threshold
        led.value = False

# Function to send data using UART
def send_data(data):
    try:
        uart.write(bytes(f"{data:.2f}\n", "utf-8")) # "utf-8" is a standard used to represent characters from different writing styles
        print(f"Data sent: {data:.2f}")
    except Exception as e:
        print(f"Error sending data through UART: {e}")
    time.sleep(0.01)  # Short delay to allow UART buffer to clear

while True:
    try:
        # Read phototransistor voltage
        voltage = get_voltage(phototransistor)
        # Control the LED based on the voltage
        control_led(voltage)
        # Sending the voltage through UART
        send_data(voltage)
    except Exception as e:
        print(f"Error reading sensor or sending data: {e}")
    time.sleep(0.1)  # Delay to control the frequency of readings
