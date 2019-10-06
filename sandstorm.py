#!/usr/bin/python3

from rtttl import parse_rtttl
from gpiozero import LED, Button, TonalBuzzer
from time import sleep
import sys, os, random

if sys.argv[1] == "-r":
    file_name = random.choice(os.listdir("/home/pi/Code/python/buzzer_dj/rtttl/"))
else:
    file_name = sys.argv[1] + ".txt"

file_path = "/home/pi/Code/python/buzzer_dj/rtttl/" + file_name
m_file = open(file_path, "r")
content = m_file.read()
m_file.close()
print(content)

darude = parse_rtttl(content)

button = Button(12)
buzzer = TonalBuzzer(26)

red_led = LED(21)
amber_led = LED(20)
green_led = LED(16)

def leds_off():
    red_led.off()
    amber_led.off()
    green_led.off()

max_tone = 880
max_note = 0
min_note = 1000

for note in darude['notes']:
    if note['frequency'] > max_note:
        max_note = note['frequency']
    if note['frequency'] < min_note:
        min_note = note['frequency']
min_tone = min_note * max_tone / max_note
buff = max_tone - min_tone

print("Played by: {0}, song name: {1}".format(darude['title'], file_name.split(".")[0]))
'''
print("min={0}, max={1}".format(min_tone, max_tone))
print(min_tone + buff * 2 / 3)
print(min_tone + buff * 1 / 3)
'''
try:
    button.wait_for_press()
    for note in darude['notes']:
        correct_f = note['frequency'] * max_tone / max_note
        if correct_f > 0:
            buzzer.play(correct_f)
            if correct_f > min_tone + buff * 3/4 :
                red_led.blink(0.02, 0.02)
            elif correct_f > min_tone + buff * 2/3:
                amber_led.blink(0.04, 0.04)
            else:
                green_led.blink(0.06, 0.06)
            
        sleep(note['duration'] / 1000)
        leds_off()
        buzzer.stop()
    
    button.wait_for_release()
except KeyboardInterrupt:
    print("Exiting...")
