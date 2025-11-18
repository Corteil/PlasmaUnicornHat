# PlasmaUnicornHat
MicroPython Library for the Pimoroni Unicorn Hat based on the original Pimoroni Python Unicorn hat library. My aim is for the library to be 100% compatible.
The original library can be found here https://github.com/pimoroni/unicorn-hat, most of the Pirates' examples will work out of the box with only changing the library import statment. 
## Why?
I was lucky to be given a number of Unicorn hats by Pimoroni to pass on for people to make cool projects, one of them a youth member of the Cambridge Makespace Coder Dojo wanted to use the Unicorn hat with the Pimoroni Plasma 2350 W, she is/was trying to combine examples from the original Python and the Pimoroni Galactic Uncorn examples for a project. The brick wall she was hitting was that the original library was writen for python on the Raspberry Pi, not the RP2040 or RP2350 chips used on the Plasma and Raspberry Pi Picos running Pirate MicroPython. It would also be helfull for my personal projects.
## What different?
in use you should not see any difference, you may have issuses between the differances between MicroPython and Python plus any libraries used. For example: some of the Pimoroni examples use the colorsys library for converting the HSV colour system to RGB values. There is not a verison of this library available for MicroPython*, therefore the examples using this library will not run. Other differances is that the Plasma library does not have a brightness fuction for Neopixels also the `show()` function was redundant as the Neopixels are updated in real time, I rewriten the library to reimplement the `show()` function plus added a function to turn on/off the auto write function.

\* I have writting a basic library that replicates this single function and have included it here, to use it `import hsvToRGB as colorsys` :-)

## How to use the library
There is a couple of ways to use the library, first way is to rename plasmaunicornhat.py to unicornhat.py you will need to place the rename file in the 'lib' folder or in the same location as the code you wish to run.
the next option is to `import plasmaunicornhat as unicorn`, place plasmaunicornhat in the 'lib' folder or the same location as your code.

`unicorn.set_neopixel_auto_write(True)` turns on the auto-write and `False` will turn auto-write off when plasmaunicornhat is imported as unicorn.

## What's left?
The `set_gamma()` and `disable_gamma()` functions have not yet been implemented and will generate errors if called.

