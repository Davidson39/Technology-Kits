#This code is for the Bicycle Data project.
#Find instructions at https://bucknellmakers.dozuki.com/Guide/Bicycle+Data+Measurement/285?lang=en
#Eli Foster 7/4/24

import board
import displayio
import terminalio
from i2cdisplaybus import I2CDisplayBus
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_adxl34x
import time

displayio.release_displays()

oled_reset = board.D9

# Use for I2C
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
HEIGHT = 64
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=HEIGHT)



accel = adafruit_adxl34x.ADXL343(i2c)

# Make the display context
splash = displayio.Group()
display.root_group = splash

bitmap = displayio.OnDiskBitmap("/bike.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x = 0, y =35 )
splash.append(tile_grid)
while True:
    (X, Y, Z) = accel.acceleration
    angle = Y / 9.8
    text1 = "Angle: "+str(round(abs(angle), 2)*90) + "*"
    text2 = "Acceleration: " + str(round(X, 1)) + "G"


    text_area1 = label.Label(
        terminalio.FONT, text=text1, color=0xFFFFFF, x=7, y=HEIGHT // 4
)
    text_area2 = label.Label(
        terminalio.FONT, text=text2, color=0xFFFFFF, x=7, y=(HEIGHT // 2) -5
)
    splash.append(text_area1)
    splash.append(text_area2)

    time.sleep(.1)
    splash.pop()
    splash.pop()
    pass
