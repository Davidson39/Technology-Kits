# This is the main code that will play a wav file 
# Libraries 
import audiocore
import board
import audiobusio
import adafruit_sdcard
import storage
import busio
import digitalio
import time

# Use any pin that is not taken by SPI or I2S 
SD_CS = board.D9


# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# wav file that will be played
wave_file = open("/sd/fanfare2.wav", "rb")
wave = audiocore.WaveFile(wave_file)

audio = audiobusio.I2SOut(board.D1, board.D10, board.D11)

while True:
    audio.play(wave)
    time.sleep(5)
    audio.stop()
    time.sleep(.1)

