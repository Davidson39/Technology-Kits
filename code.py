# Run this code to test and make sure your bluetooth is working correctly
import time
import busio
import board
from digitalio import DigitalInOut
from adafruit_bluefruitspi import BluefruitSPI
from digitalio import DigitalInOut, Direction

spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.D6)
irq = DigitalInOut(board.D11)
rst = DigitalInOut(board.D10)
bluefruit = BluefruitSPI(spi_bus, cs, irq, rst, debug=False)

# Setup for onboard led
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Initialize the device and perform a factory reset
print("Initializing the Bluefruit LE SPI Friend module")
bluefruit.init()
bluefruit.command_check_OK(b'AT+FACTORYRESET', delay=1)

# Print the response to 'ATI' (info request) as a string
print(str(bluefruit.command_check_OK(b'ATI'), 'utf-8'))

# Change advertised name
bluefruit.command_check_OK(b'AT+GAPDEVNAME=BlinkaBLE')

while True:
    print("Waiting for a connection to Bluefruit LE Connect ...")
    # Wait for a connection ...
    dotcount = 0
    while not bluefruit.connected:
        print(".", end="")
        dotcount = (dotcount + 1) % 80
        if dotcount == 79:
            print("")
        time.sleep(0.5)

    # Once connected, check for incoming BLE UART data
    print("\n *Connected!*")
    connection_timestamp = time.monotonic()
    while True:
        # Check our connection status every 3 seconds
        if time.monotonic() - connection_timestamp > 3:
            connection_timestamp = time.monotonic()
            if not bluefruit.connected:
                break

        # OK we're still connected, see if we have any data waiting
        resp = bluefruit.uart_rx()
        if not resp:
            continue  # nothin'
        print("Read %d bytes: %s" % (len(resp), resp))
        command = resp.decode('utf-8').strip()

        # Now write it!
        if command == "LED ON":
            led.value = True
            print("LED turned ON")
        elif command == "LED OFF":
            led.value = False
            print("LED turned OFF")

    print("Connection lost.")
