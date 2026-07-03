import time
import sys
import random
from gpiozero import LED

sys.path.append("/usr/bin")
from rq_led_utils import (
    get_led_config,
    create_neopixel_strip,
    chunked_show,
    map_xy_to_pixel,
)

# --------------------------------------------------
# Setup
# --------------------------------------------------

led = LED(4)        # LED with reference to the GPIO Pin

config = get_led_config()

pixels = create_neopixel_strip(
    config["led_count"],
    config["pixel_order"],
    brightness=config["led_default_brightness"],
)

BLACK = (0, 0, 0)
WHITE = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = [RED, GREEN, BLUE]

WAIT = 3


def clear():
    pixels.fill(BLACK)
    chunked_show(pixels)


def set_pixel(x, y, color):
    idx = map_xy_to_pixel(x, y)
    if idx is not None:
        pixels[idx] = color


# --------------------------------------------------
# Example 1 - Horizontal Line
# --------------------------------------------------

def horizontal_line(color=GREEN):
    clear()

    y = 0

    for y in range(8):
        for x in range(24):
            set_pixel(x, y, color)
        #time.sleep(0.25)
        chunked_show(pixels)
        y += 1



# --------------------------------------------------
# Example 2 - Vertical Line
# --------------------------------------------------

def vertical_line(color=RED):
    clear()

    x = 0
    for x in range(24):
        for y in range(8):
            set_pixel(x, y, color)
        chunked_show(pixels)
        time.sleep(0.25)
        clear()
        x += 1
    x = 1
    for x in range(24):
        for y in range(8):
            set_pixel(23 - x, y, color)
        chunked_show(pixels)
        time.sleep(0.2)
        clear()
        x += 1


# --------------------------------------------------
# Example 3 - "Quantum Measurement"
# --------------------------------------------------

def border_background():
    draw_sprite_24x8(BLUE_FADE, 0, 0)
    draw_sprite_24x8(BLUE_FADE, 8, 0)
    draw_sprite_24x8(BLUE_FADE, 16, 0)
    chunked_show(pixels)
    
    for x2 in range(28):
        set_pixel(x2, 6, (8,8,8))
        set_pixel(x2, 1, (8,8,8))
        set_pixel(x2, 2, (4,4,4))
        set_pixel(x2, 3, (4,4,4))
        set_pixel(x2, 4, (4,4,4))
        set_pixel(x2, 5, (4,4,4))
    chunked_show(pixels)

def quantum_measurement():
    
    border_background()

    y = 3  # Top row of the 2x2 blocks
    
    for _ in range(30):
        # Generate a random 8-bit measurement
        measurement = "".join(random.choice("01") for _ in range(8))
        print("Measurement:", measurement)

        for qubit, bit in enumerate(measurement):

            x = qubit * 3  # 2-pixel block + 1-pixel gap

            if bit == "1":
                colour = GREEN
            else:
                colour = (40, 40, 40)  # Dim white
            
            # Draw a 2x2 block
            for dx in range(2):
                for dy in range(2):
                    set_pixel(x + dx, y + dy, colour)

        chunked_show(pixels)
        time.sleep(0.5)
        
        
def display_binary_message(message, delay=1, compact=False):
    
    border_background()
    
    y = 3

    for ch in message.upper():

        bits = format(ord(ch), "08b")

        print(f"{ch}: {bits}")

        for i, bit in enumerate(bits):

            colour = GREEN if bit == "1" else (40, 40, 40)

            if compact:
                # 16 pixels wide, centred
                x = 4 + (i * 2)
            else:
                # 24 pixels wide with gaps
                x = i * 3

            for dx in range(2):
                for dy in range(2):
                    set_pixel(x + dx, y + dy, colour)

        chunked_show(pixels)
        time.sleep(delay)
        
        for x2 in range(28):
            set_pixel(x2, 3, (4,4,4))
            set_pixel(x2, 4, (4,4,4))

        chunked_show(pixels)

# --------------------------------------------------
# Example 4 - "SHU Lettering"
# --------------------------------------------------

SHU_COLOURS = [
    (99, 37, 61),    # Purple
    (216, 24, 97),    # Teal
    (103, 33, 70),     # Pink
]

FONT = {

    "S": [
    "00111110",
    "01111111",
    "01110000",
    "01111110",
    "00111111",
    "00000111",
    "01111111",
    "00111110",
    ],
    
    "H": [
    "01100011",
    "01100011",
    "01100011",
    "01111111",
    "01111111",
    "01100011",
    "01100011",
    "01100011",
    ],
    
    "U": [
    "0110011",
    "0110011",
    "0110011",
    "0110011",
    "0110011",
    "0110011",
    "0111111",
    "0011110",
    ],
    
    
    "Hi": [
    "00000000",
    "11011011",
    "11011000",
    "11111011",
    "11111011",
    "11011011",
    "11011011",
    "00000000",
    ],
    
    
    ":)": [
    "00000000",
    "01100110",
    "01100110",
    "00000000",
    "01100110",
    "00111100",
    "00000000",
    "00000000",
    ],

}

def draw_char(x0, y0, ch, colour):
    bitmap = FONT[ch]
    height = len(bitmap)

    for y, row in enumerate(bitmap):
        for x, pixel in enumerate(row):
            if pixel == "1":
                set_pixel(x0 + x, y0 + (height - 1 - y), colour)

def shu_logo(delay=2):

    for colour in SHU_COLOURS:

        #clear()

        draw_char(0, 0, "S", colour)
        #chunked_show(pixels)
        draw_char(8, 0, "H", colour)
        #chunked_show(pixels)
        draw_char(16, 0, "U", colour)
        chunked_show(pixels)


        time.sleep(delay)


# --------------------------------------------------
#  Random Blue Sparkles
# --------------------------------------------------

def random_blue_sparkle(frames=5, pixels_per_frame=35, color=BLUE):

    for _ in range(frames):

        # Choose random unique pixels
        positions = random.sample(
            [(x, y) for x in range(24) for y in range(8)],
            pixels_per_frame
        )
        clear()
        for x, y in positions:
            brightness = random.randint(10, 255)
            if color == BLUE:
                set_pixel(x, y, (0, 0, brightness))
            else:
                set_pixel(x, y, (brightness, brightness, brightness))
            chunked_show(pixels)
        time.sleep(3) 



def draw_sprite_24x8(sprite, x0=0, y0=0):

    width = 8   # inferred from your data structure (64 = 8x8)

    for i, colour in enumerate(sprite):

        x = i % width
        y = i // width

        if y >= 8:
            continue

        set_pixel(x0 + x, y0 + (7 - y), tuple(colour))
        
BLUE_FADE = [
#[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,159],[0,0,159],[0,0,159],[0,0,159],[0,0,159],[0,0,159],[0,0,159],[0,0,159],[0,0,191],[0,0,191],[0,0,191],[0,0,191],[0,0,191],[0,0,191],[0,0,191],[0,0,191],[0,0,223],[0,0,223],[0,0,223],[0,0,223],[0,0,223],[0,0,223],[0,0,223],[0,0,223],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,0,255]
[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127]
]
BLUE_FADE_STRIPE = [
[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[0,0,31],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[0,0,95],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127],[0,0,127]
]
BLUE_FADE_LIGHT = [
[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,8],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,16],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,24],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32],[0,0,32]
]

# --------------------------------------------------
# Main
# --------------------------------------------------

try:

    led.on()       
    
    while True:
        
        
        draw_sprite_24x8(BLUE_FADE, 0, 0)
        draw_sprite_24x8(BLUE_FADE, 8, 0)
        draw_sprite_24x8(BLUE_FADE, 16, 0)
        chunked_show(pixels)
        time.sleep(WAIT)

        print("Showing SHU...")
        shu_logo(0)
        time.sleep(WAIT)

        print("Showing blue sparkle...")
        repeat = random.randint(3,8)
        sparkles = random.randint(48,96)
        random_blue_sparkle(repeat, sparkles)

        #print("Showing quantum measurement...")
        #quantum_measurement()
        #time.sleep(WAIT)
        
        print("Showing binary message (HALLAM in ASCII (eg: H=72, A=65, L=76 ...")
        display_binary_message("HALLAM")
        time.sleep(WAIT) 
   
        color = (random.randint(0,127),random.randint(0,127),random.randint(35,127))
        print(f"Showing horizontal line... [color={color}]")
        #color = random.choice(COLORS)
        horizontal_line(color)
        time.sleep(WAIT)

        print("Showing vertical line...")
        color = random.choice(COLORS)
        vertical_line(color)
        time.sleep(WAIT)


finally:
    clear()
