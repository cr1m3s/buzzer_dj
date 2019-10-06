#!/usr/bin/python3

from rtttl import parse_rtttl
from gpiozero.tones import Tone
from gpiozero import LED, Button, TonalBuzzer, Buzzer
from time import sleep
import sys, os, random

buzzer = TonalBuzzer(26)
max_tone = buzzer.max_tone.frequency - 100
min_tone = buzzer.min_tone.frequency + 10
max_note = 0
min_note = 1000
m_button = Button(12)

def generating_file(file_var):
    file_name = ""

    if file_var == "-r":
        file_name = random.choice(os.listdir("/home/pi/Code/python/buzzer_dj/rtttl/"))
    else:
        file_name = sys.argv[1] + ".txt"

    return file_name

def content_gen(file_name):
    file_path = "/home/pi/Code/python/buzzer_dj/rtttl/" + file_name
    melody_file = open(file_path, "r")
    file_content = melody_file.read()
    melody_file.close()
    return file_content 

def tones_finder(melody):
    global max_note
    global min_note
    for note in melody['notes']:
        if note['frequency'] > max_note:
            max_note = note['frequency']
        if note['frequency'] <  min_note and note['frequency'] > 0:
            min_note = note['frequency']


def melody_player(melody): 
    global min_tone

    red_led = LED(21)
    amber_led = LED(20)
    green_led = LED(16)
    blue_led = LED(6)
    leds = [red_led, amber_led, green_led, blue_led]

    my_min_tone = min_note * max_tone / max_note
    tone_buffer = max_tone - min_tone
    note_diff = max_tone / max_note

    for note in melody['notes']:
        correct_note = note['frequency'] * note_diff
        
        if correct_note > 0:
            if correct_note < min_tone:
                correct_note = min_tone
            print(correct_note)
            buzzer.play(correct_note)
            if correct_note > min_tone + tone_buffer * 0.75:
                red_led.blink(0.02, 0.02)
            elif correct_note > min_tone + tone_buffer * 0.5:
                amber_led.blink(0.04, 0.04)
            elif correct_note > min_tone + tone_buffer * 0.25:
                green_led.blink(0.06, 0.06)
            else:
                blue_led.blink(0.08, 0.08)
        sleep(note['duration'] / 1000)
        for led in leds:
            led.off()
        buzzer.stop()

try:
    print("Press button for start:")
    while True:
        
        if m_button.is_pressed:
            file_name = generating_file(sys.argv[1])
            print(file_name)
            content = parse_rtttl(content_gen(file_name))
            tones_finder(content)
            print("Played by: {0}, song name: {1}".format(content['title'],\
                file_name.split(".")[0]))
            melody_player(content)
            print("Press button again if you want to hear something again")
            print("For exit use ctrl+c")
except KeyboardInterrupt:
    print("Exiting...")
