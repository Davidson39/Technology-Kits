# Run this code to see if your camera is functioning correctly
import time
import board
import busio
import digitalio
import storage
import adafruit_vc0706
import adafruit_sdcard

# Configuration
SD_CS_PIN = board.D4
IMAGE_FILE = "/sd/image.jpg"

# Setup SPI bus (hardware SPI)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Setup SD card and mount it in the filesystem
sd_cs = digitalio.DigitalInOut(SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create a serial connection for the VC0706 connection
uart = busio.UART(board.TX, board.RX, baudrate=115200)
vc0706 = adafruit_vc0706.VC0706(uart)

# Function to capture and save an image
def capture_image():
    print("Taking a picture in 3 seconds...")
    time.sleep(3)
    print("SNAP!")
    if not vc0706.take_picture():
        raise RuntimeError("Failed to take picture!")

    frame_length = vc0706.frame_length
    print("Picture size (bytes): {}".format(frame_length))

    with open(IMAGE_FILE, "wb") as outfile:
        while frame_length > 0:
            to_read = min(frame_length, 32)
            copy_buffer = bytearray(to_read)
            if vc0706.read_picture_into(copy_buffer) == 0:
                raise RuntimeError("Failed to read picture frame data!")
            outfile.write(copy_buffer)
            frame_length -= 32
    print("Image saved to SD card.")
    
# Main function
capture_image()
