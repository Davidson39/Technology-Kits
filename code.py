#Thermometer project code
#Eli Foster 7/5/24


import board
import displayio
import adafruit_displayio_sh1107
import adafruit_am2320
import adafruit_display_text
from adafruit_display_text import label
import terminalio
import time

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

displayio.release_displays()
# oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = I2CDisplayBus(i2c, device_address=0x3d)
time.sleep(.1)

#initialize sensor
am = adafruit_am2320.AM2320(i2c)
print(am.temperature)

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

#initialize display
display = adafruit_displayio_sh1107.SH1107(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

# Make the display context
splash = displayio.Group()
display.root_group = splash



# Draw baseline
bitmap = displayio.OnDiskBitmap("/thermometer.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader = bitmap.pixel_shader)
splash.append(tile_grid)


while True:
    #insert temperature text
    temp = am.temperature
    text1 = "Temperature: " + str(temp) + " degrees C"  # overly long to see where it clips
    text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=8)
    splash.append(text_area)

    #Find correct temperature
    if temp > 32.5:
        splash.insert(0, displayio.TileGrid(displayio.OnDiskBitmap("/thermTOP.bmp"), pixel_shader = bitmap.pixel_shader))
        time.sleep(5)
    elif temp > 25:
        splash.insert(0, displayio.TileGrid(displayio.OnDiskBitmap("/thermMID.bmp"), pixel_shader = bitmap.pixel_shader))
        time.sleep(5)
    elif temp > 20:
        splash.insert(0, displayio.TileGrid(displayio.OnDiskBitmap("/thermBOT.bmp"), pixel_shader = bitmap.pixel_shader))
        time.sleep(5)
    elif temp > 15:
        splash.insert(0, displayio.TileGrid(displayio.OnDiskBitmap("/thermBOTHALF.bmp"), pixel_shader = bitmap.pixel_shader))
        time.sleep(5)
    else:
        splash.insert(0, displayio.TileGrid(displayio.OnDiskBitmap("/thermometer.bmp"), pixel_shader = bitmap.pixel_shader))
        time.sleep(5)
    splash.pop()
    splash.pop()
    pass
