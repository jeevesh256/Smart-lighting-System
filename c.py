import sounddevice as sd
import numpy as np
import RPi.GPIO as GPIO

LED_PIN = 13
SOUND_THRESHOLD = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

def turn_on_light():
    GPIO.output(LED_PIN, GPIO.HIGH)

def turn_off_light():
    GPIO.output(LED_PIN, GPIO.LOW)

def detect_sound(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > SOUND_THRESHOLD:
        turn_on_light()
    else:
        turn_off_light()

def listen_for_sound():
    stream = sd.InputStream(callback=detect_sound)
    with stream:
        print("Listening for sounds...")
        while True:
            pass

if __name__ == "__main__":
    listen_for_sound()
