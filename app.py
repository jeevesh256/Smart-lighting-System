from flask import Flask, render_template
import RPi.GPIO as GPIO
import subprocess

app = Flask(__name__)

LED_PIN = 13  

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  

light_state = False
motion_mode = False
party_mode = False
motion_process = None
party_process = None

@app.route('/')
def index():
    global light_state, motion_mode, party_mode
    return render_template('index.html', light_state=light_state, motion_mode=motion_mode, party_mode=party_mode)

@app.route('/toggle_light')
def toggle_light():
    global light_state
    light_state = not light_state
    GPIO.output(LED_PIN, GPIO.HIGH if light_state else GPIO.LOW)
    return index()

@app.route('/run_pir')
def run_pir():
    global motion_mode, motion_process

    motion_mode = not motion_mode

    if motion_mode:
        motion_process = subprocess.Popen(['python', 'pir.py'])
    else:
        if motion_process:
            motion_process.terminate()

    return index()

@app.route('/toggle_party')
def toggle_party():
    global party_mode, party_process
    party_mode = not party_mode

    if party_mode:
        party_process = subprocess.Popen(['python', 'c.py'])
    else:
        if party_process:
            party_process.terminate()

    return index()

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    finally:
        GPIO.cleanup()
