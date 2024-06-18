
import RPi.GPIO as GPIO
import time

# Encoder pins
encoder_a_pin = 17  # GPIO pin connected to encoder A output
encoder_b_pin = 18  # GPIO pin connected to encoder B output

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder_b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to store the encoder position
position = 0
last_encoded = 0

# Constants
DISTANCE_PER_PULSE = 0.01  # mm per pulse, as calculated

def update_position(channel):
    global position, last_encoded

    # Read the encoder pins
    MSB = GPIO.input(encoder_a_pin)
    LSB = GPIO.input(encoder_b_pin)

    encoded = (MSB << 1) | LSB
    delta = (encoded - last_encoded) % 4

    if delta == 1:
        position += 1
    elif delta == 3:
        position -= 1

    last_encoded = encoded

# Interrupts for the encoder
GPIO.add_event_detect(encoder_a_pin, GPIO.BOTH, callback=update_position)
GPIO.add_event_detect(encoder_b_pin, GPIO.BOTH, callback=update_position)

try:
    while True:
        translatory_position = position * DISTANCE_PER_PULSE
        print(f"Translatory Position: {translatory_position} mm")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()