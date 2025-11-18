import time
import math
from machine import Pin

import plasma



COLORS = {
    'red':(255,0,0),
    'lime':(0,255,0),
    'blue':(0,0,255),
    'yellow':(255,255,0),
    'magenta':(255,0,255),
    'cyan':(0,255,255),
    'black':(0,0,0),
    'white':(255,255,255),
    'gray':(127,127,127),
    'grey':(127,127,127),
    'silver':(192,192,192),
    'maroon':(128,0,0),
    'olive':(128,128,0),
    'green':(0,128,0),
    'purple':(128,0,128),
    'teal':(0,128,128),
    'navy':(0,0,128),
    'orange':(255,165,0),
    'gold':(255,215,0),
    'purple':(128,0,128),
    'indigo':(75,0,130)
}

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

LED_GAMMA = [
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11,
11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
19, 19, 20, 21, 21, 22, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28,
29, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 37, 38, 39, 40,
40, 41, 42, 43, 44, 45, 46, 46, 47, 48, 49, 50, 51, 52, 53, 54,
55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89,
90, 91, 93, 94, 95, 96, 98, 99,100,102,103,104,106,107,109,110,
111,113,114,116,117,119,120,121,123,124,126,128,129,131,132,134,
135,137,138,140,142,143,145,146,148,150,151,153,155,157,158,160,
162,163,165,167,169,170,172,174,176,178,179,181,183,185,187,189,
191,193,194,196,198,200,202,204,206,208,210,212,214,216,218,220,
222,224,227,229,231,233,235,237,239,241,244,246,248,250,252,255]


# variables from the Pimoroni Unicorn Hat

"""
Store the rotation of UnicornHat, defaults to
0 which places 0,0 on the top left with the B+
HDMI port facing downwards
"""
_rotation = 0
_requested_rotation = 0
_wx = 8
_wy = 8
_map = []
_pixels = [(0,0,0) for x in range(64)]
_is_setup = False

# End of Pimoroni variables

# set up the Pico W's onboard LED
#pico_led = Pin('LED', Pin.OUT)

# unicorn setup

unicorn_hat = None
neopixel_brightness = 0.5
orientation = 0
neopixel_auto_write = False


unicorn_pixel_address = ([7 , 6 , 5 , 4 , 3 , 2 , 1 , 0 ],
                         [8 , 9 , 10, 11, 12, 13, 14, 15],
                         [23, 22, 21, 20, 19, 18, 17, 16],
                         [24, 25, 26, 27, 28, 29, 30, 31],
                         [39, 38, 37, 36, 35, 34, 33, 32],
                         [40, 41, 42, 43, 44, 45, 46, 47],
                         [55, 54, 53, 52, 51, 50, 49, 48],
                         [56, 57, 58, 59, 60, 61, 62, 63])
'''

unicorn_pixel_address = ([0, 15, 16, 31, 32, 47, 48, 63],
                         [1, 14, 17, 30, 33, 46, 49, 62],
                         [2, 13, 18, 29, 34, 45, 50, 61],
                         [3, 12, 19, 28, 35, 44, 51, 60],
                         [4, 11, 20, 27, 36, 43, 52, 59],
                         [5, 10, 21, 26, 37, 42, 53, 58],
                         [6, 9, 22, 25, 38, 41, 54, 57],
                         [7, 8, 23, 24, 39, 40, 55, 56])
'''

"""
Store a map of pixel indexes for
translating x, y coordinates.
"""

HAT = [
    [7 , 6 , 5 , 4 , 3 , 2 , 1 , 0 ],
    [8 , 9 , 10, 11, 12, 13, 14, 15],
    [23, 22, 21, 20, 19, 18, 17, 16],
    [24, 25, 26, 27, 28, 29, 30, 31],
    [39, 38, 37, 36, 35, 34, 33, 32],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [55, 54, 53, 52, 51, 50, 49, 48],
    [56, 57, 58, 59, 60, 61, 62, 63]
]

PHAT_VERTICAL = [
    [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 ],
    [8 , 9 , 10, 11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20, 21, 22, 23],
    [24, 25, 26, 27, 28, 29, 30, 31]
]

PHAT = [
    [24, 16, 8,  0],
    [25, 17, 9,  1],
    [26, 18, 10, 2],
    [27, 19, 11, 3],
    [28, 20, 12, 4],
    [29, 21, 13, 5],
    [30, 22, 14, 6],
    [31, 23, 15, 7]
]

AUTO = None


'''
# UNicorn hat library functions.
unicornhat.brightness(b=0.2)
unicornhat.clear()
unicornhat.get_brightness()
unicornhat.get_index_from_xy(x, y)[source]
unicornhat.get_pixel(x, y)[source]
unicornhat.get_pixels()[source]
unicornhat.get_shape()[source]
unicornhat.off()
unicornhat.rotation(r=0)[source]
unicornhat.set_all(r, g, b)
unicornhat.set_layout(pixel_map=None)[source]
unicornhat.set_pixel(x, y, r, g, b)[source]
unicornhat.set_pixel_hsv(x, y, h, s, v)[source]
unicornhat.set_pixels(pixels)
unicornhat.shade_pixels(shader)[source]
unicornhat.show()
'''

def setup():
    global unicorn_hat, _is_setup, neopixel_auto_write
    if _is_setup:
        return

    unicorn_hat = plasma.WS2812(LED_COUNT, color_order=plasma.COLOR_ORDER_GRB)
    #unicorn_hat.brightness = neopixel_brightness
    
    # start updating the LED strip
    unicorn_hat.start()

    set_layout(HAT)
    
    _is_setup = True

    print("setup done")

def set_layout(pixel_map = AUTO):
    """Set the layout to Unicorn HAT or Unicorn pHAT

    Note: auto detection relies upon the HAT EEPROM. Your Unicorn HAT
    must be connected before boot to successfully auto detect.

    :param pixel_map: Choose the layout to set, can be either HAT, PHAT, PHAT_VERTICAL or AUTO
    """

    global _map

    if pixel_map is None:
        pixel_map = HAT # Assume HAT
        """
        # Raspberry Pi OS code to check for presence of Unicorn HAT
        try:
            product = open("/proc/device-tree/hat/product","r").read().strip()
            if product[:11] == "Unicorn HAT":
                pixel_map = HAT

        except IOError:
            pass
        """
    _map = pixel_map
    
def get_shape():
    """Returns the shape (width, height) of the display"""

    global _map

    setup() # Shape is unset until this is called
    return (len(_map), len(_map[0]))

def _clean_shutdown():
    """Registered at exit to ensure Neopixels cleans up after itself
    and all pixels are turned off.
    """

    off()
    print("Goodbye")
    
    
def rotation(r=0):
    """Set the display rotation

    :param r: Specify the rotation in degrees: 0, 90, 180 or 270
    """

    global _map
    global _rotation
    global _requested_rotation

    setup()
    if r in [0, 90, 180, 270]:
        _requested_rotation=r
        wx = len(_map)
        wy = len(_map[0])

        if wx == wy:
          _rotation = r

        else:
          if r in [0, 180]:
            _map = PHAT
            _rotation = r
          else:
            _map = PHAT_VERTICAL
            _rotation = r-90

        return True

    else:
        raise ValueError('Rotation must be 0, 90, 180 or 270 degrees')


def get_rotation():
    """Get the display rotation value

    Returns an integer, either 0, 90, 180 or 270
    """

    return _requested_rotation

def brightness(b= 0.2):
    
    """Set the display brightness between 0.0 and 1.0

    0.2 is highly recommended, UnicornHat can get painfully bright!

    :param b: Brightness from 0.0 to 1.0 (default 0.2)
    """
    global neopixel_brightness
    setup()

    if b > 1 or b < 0:
        raise ValueError('Brightness must be between 0.0 and 1.0')

    """Absolute max brightness has been capped to 50%, do not change
    this unless you know what you're doing.
    UnicornHAT draws too much current above 50%."""

    if b < 0.2:
        print("Warning: Low brightness chosen, your UnicornHAT might not light up!")

    neopixel_brightness = b

def get_brightness():
    return neopixel_brightness


def clear():

    """Clear the buffer"""

    setup()

    for index in range(64):
        _pixels[index] = (0, 0, 0)


def off():
    """Clear the buffer and immediately update UnicornHat

    Turns off all pixels.
    """
    clear()
    show()
    
    
def get_index_from_xy(x, y):
    
    #index = find_pixel(x, y)
    
    """Convert an x, y value to an index on the display

    :param x: Horizontal position from 0 to 7
    :param y: Vertical position from 0 to 7
    """

    setup()

    wx = len(_map) - 1
    wy = len(_map[0]) - 1

    y = (wy)-y

    if _rotation == 90 and wx == wy:
        x, y = y, (wx)-x
    elif _rotation == 180:
        x, y = (wx)-x, (wy)-y
    elif _rotation == 270 and wx == wy:
        x, y = (wy)-y, x

    try:
        index = _map[x][y]
    except IndexError:
        index = None
    
    return index


def find_pixel(X, Y):
    # helper function instead of get_index_from_xy
    #print(f"find pixel X: {X} Y: {Y}")
    pixel = unicorn_pixel_address[Y][X]
    #print(f"pixel: {pixel}")
    return pixel


def hsvToRGB(h, s, v):
    """Convert HSV color space to RGB color space
    
    @param h: Hue
    @param s: Saturation
    @param v: Value
    return (r, g, b)  as a value beween 0.0 and 1.0
    """
   
    hi = math.floor(h / 60.0) % 6
    f =  (h / 60.0) - math.floor(h / 60.0)
    p = v * (1.0 - s)
    q = v * (1.0 - (f*s))
    t = v * (1.0 - ((1.0 - f) * s))
    return {
            0: [v, t, p],
            1: [q, v, p],
            2: [p, v, t],
            3: [p, q, v],
            4: [t, p, v],
            5: [v, p, q],
    }[hi]
    


def set_pixel_hsv(x, y, h, s=None, v=None):
    """Set a single pixel to a colour using HSV

    :param x: Horizontal position from 0 to 7
    :param y: Veritcal position from 0 to 7
    :param h: Hue from 0.0 to 1.0 ( IE: degrees around hue wheel/360.0 )
    :param s: Saturation from 0.0 to 1.0
    :param v: Value (also known as brightness) from 0.0 to 1.0
    """

    if type(h) is tuple:
        h, s, v = h

    r, g, b = [int(n*255) for n in hsvToRGB(h, s, v)]

    set_pixel(x, y, r, g, b)


def set_pixel(x, y, r, g=None, b=None):
    """Set a single pixel to RGB colour

    :param x: Horizontal position from 0 to 7
    :param y: Veritcal position from 0 to 7
    :param r: Amount of red from 0 to 255
    :param g: Amount of green from 0 to 255
    :param b: Amount of blue from 0 to 255
    """
    
    setup()
    
    
    if type(r) is tuple:
        r, g, b = r
    
    elif type(r) is str:
        try:
            r, g, b = COLORS[r.lower()]
        
        except KeyError:
            raise ValueError('Invalid color!')
    index = get_index_from_xy(x, y)

    if index is not None:
        if neopixel_auto_write:
            rb = int(r * neopixel_brightness)
            gb = int(g * neopixel_brightness)
            bb = int(b * neopixel_brightness)
            unicorn_hat.set_rgb(index, rb, gb, bb)
        
        _pixels[index] = (r, g, b)
    
    #pixel = find_pixel(x, y)
    #unicorn_hat.set_rgb(pixel, r, g, b)
        
def get_pixel(x, y):
    """Get the RGB value of a single pixel

    :param x: Horizontal position from 0 to 7
    :param y: Veritcal position from 0 to 7
    """

    index = get_index_from_xy(x, y)
    if index is not None:
        return _pixels[index]


def set_all(r, g=None, b=None):
    """Set all pixels to a specific colour"""

    shade_pixels(lambda x, y: (r, g, b))
'''
def set_all(r, g, b):
    
    for pixel in range(LED_COUNT):
        unicorn_hat.set_rgb(pixel, r, g, b)
'''

def shade_pixels(shader, *args):
    """Set all pixels using a pixel shader style function

    :param shader: A function which accepts the x and y positions of a pixel and returns a tuple (r, g, b)

    For example, this would be synonymous to clear::

        set_pixels(lambda x, y: return 0,0,0)

    Or perhaps we want to map red along the horizontal axis, and blue along the vertical::

        set_pixels(lambda x, y: return (x/7.0) * 255, 0, (y/7.0) * 255)
    """
   
    width, height = get_shape()
    for x in range(width):
        for y in range(height):
            r, g, b = shader(x, y, *args)
            set_pixel(x, y, r, g, b)    
    
def set_pixels(pixels):
    """Set all pixels using an array of `get_shape()`"""
    
    shade_pixels(lambda x, y: pixels[y][x])
    

def get_pixels():
    """Get the RGB value of all pixels in a 7x7x3 2d array of tuples"""

    width, height = get_shape()

    return [[get_pixel(x, y) for x in range(width)] for y in range(height)]

def show_pixel(x, y, r, g=None, b=None):
    """Set a single pixel to RGB colour

    :param x: Horizontal position from 0 to 7
    :param y: Veritcal position from 0 to 7
    :param r: Amount of red from 0 to 255
    :param g: Amount of green from 0 to 255
    :param b: Amount of blue from 0 to 255
    """
    
    setup()
    
    if type(r) is tuple:
        r, g, b = r
    
    elif type(r) is str:
        try:
            r, g, b = COLORS[r.lower()]
        
        except KeyError:
            raise ValueError('Invalid color!')
    index = get_index_from_xy(x, y)

    if index is not None:
        rb = int(r * neopixel_brightness)
        gb = int(g * neopixel_brightness)
        bb = int(b * neopixel_brightness)
        unicorn_hat.set_rgb(index, rb, gb, bb)
        _pixels[index] = (r, g, b)
    
    #pixel = find_pixel(x, y)
    #unicorn_hat.set_rgb(pixel, r, g, b)

def show():
    for x in range(8):
        for y in range(8):
            colour = get_pixel(x, y)
            #print(f"X: {x} Y: {y} colour: {colour}")
            show_pixel(x, y, colour)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def set_neopixel_auto_write(setting):
    global neopixel_auto_write, _is_setup
    neopixel_auto_write = setting
    #_is_setup = False
    #setup()

"""
# unicorn setup end
setup()
unicorn_hat.clear()
set_pixel_hsv(1, 1, 27, 0.813, 0.902)
set_pixel(2, 5, COLORS["red"])
time.sleep(1)
#fill_unicorn(0, 255, 0)
time.sleep(1)
clear()
"""