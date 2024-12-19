import sys
import termios
import tty
import signal
import cv2
import base64
import numpy as np
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
import requests
import json

id = ""
base64_data = ""

lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=1)
lcd2 = CharLCD(i2c_expander='PCF8574', address=0x27, port=4)

lcd1.cursor_pos = (0, 0)
lcd1.write_string('Selamat Datang')
lcd1.cursor_pos = (1, 0)
lcd1.write_string('Silahkan Absen')

lcd2.cursor_pos = (0, 0)
lcd2.write_string('Selamat Datang')
lcd2.cursor_pos = (1, 0)
lcd2.write_string('Silahkan Absen')

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(8)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def terminate_program(signal, frame):
    print('\nProgram dihentikan.')
    sys.exit(0)
    
def displayOne():
    lcd1.clear()
    lcd1.cursor_pos = (0, 0)
    lcd1.write_string('Halo...')
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string(digit_nama)
    lcd1.cursor_pos = (2, 0)
    lcd1.write_string(f"KELAS {kelas}")
    lcd1.cursor_pos = (3, 0)
    lcd1.write_string(f"{time}")
    sleep(4)
    lcd1.clear()
    lcd1.cursor_pos = (0, 0)
    lcd1.write_string('Selamat Datang')
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string('Silahkan Absen ')

def displayTwo():
    lcd2.clear()
    lcd2.cursor_pos = (0, 0)
    lcd2.write_string('Halo...')
    lcd2.cursor_pos = (1, 0)
    lcd2.write_string(digit_nama)
    lcd2.cursor_pos = (2, 0)
    lcd2.write_string(f"KELAS {kelas}")
    lcd2.cursor_pos = (3, 0)
    lcd2.write_string(f"{time}")
    sleep(4)
    lcd2.clear()
    lcd2.cursor_pos = (0, 0)
    lcd2.write_string('Selamat Datang')
    lcd2.cursor_pos = (1, 0)
    lcd2.write_string('Silahkan Absen ')
    
user_input = ''
all_input = ''
all_uid = ''

print('Program sedang berjalan. Tekan Ctrl+C untuk menutup program.')

signal.signal(signal.SIGINT, terminate_program)

while True:
    cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
    ch = getch()
    
    if ch:
        try:
            for _ in range(20):  
                _, _ = cap.read()
            #uid = getch()
            #if len(uid) < 8:
            #    all_uid += uid
            ret, image = cap.read()
            alpha = 1  
            beta = 2
            brightened_frame = cv2.addWeighted(image, alpha, image, 0, beta)
            #cv2.imwrite(f"{ch}.jpg", brightened_frame)
            ret, buffer = cv2.imencode('.jpg', brightened_frame)
            jpg_as_text = base64.b64encode(buffer).decode()
            sleep(1)
            #print("Base64 string: ", jpg_as_text)
            #print(ch)
            id = f"{ch}"
            base64_data = jpg_as_text
            #lcd1.write_string('Halo...')
            print("id : ",id)
            url = f"https://api.tierkun.my.id/enterexit/lf/{id}"
            
            body = {
                "capture": base64_data
            }

            response = requests.post(url, data=body)
            print("Status code: ", response.status_code)
            print("Response: ", response.json())
            msg = response.json()
            nama = msg['Nama']
            kelas = msg['Kelas']
            time = msg['Time']
            digit_nama = nama[:20]
            print(digit_nama)
            cap.release()
            cv2.destroyAllWindows()
            displayOne()
            displayTwo()
        except Exception as error:
            print(error)
            continue
        
    else:
        print(f'Input: {user_input}')
        user_input = ''
