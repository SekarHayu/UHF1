import sys
import termios
import tty
import signal
import cv2
import base64
import numpy as np
#from RPLCD import *
from time import sleep
#from RPLCD.i2c import CharLCD
import requests
import json
import warnings

warnings.simplefilter("ignore")

id = ""
base64_data = ""

#lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=4)
#lcd2 = CharLCD(i2c_expander='PCF8574', address=0x27, port=4)

sleep(1)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        c = sys.stdin.read(9)
        ch = c.strip()
        print(f"'ch : {ch}'")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def terminate_program(signal, frame):
    print('\nProgram dihentikan.')
    sys.exit(0)
"""
def displayOne(digit_nama, kelas, time):
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
    lcd1.write_string('Silahkan Tap Kartu')
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string('Identitas Anda')

def error(not_found):
    print("not found :", not_found)
    lcd1.clear()
    lcd1.cursor_pos = (0, 0)
    lcd1.write_string('Maaf...')
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string(not_found)
    lcd1.cursor_pos = (2, 0)
    sleep(4)
    lcd1.clear()
    lcd1.cursor_pos = (0, 0)
    lcd1.write_string('Silahkan Tap Kartu')
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string('Identitas Anda')
""" 
user_input = ''
all_input = ''
all_uid = ''
not_found = ''

print('Program sedang berjalan. Tekan Ctrl+C untuk menutup program.')


signal.signal(signal.SIGINT, terminate_program)



while True:
    #ch = "0c94c8f0"
    ch = getch()
    print("ID : ", ch)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
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
                "capture": base64_data,
                "typeLF": "LF4"
            }

            response = requests.post(url, data=body)
            print("url :", url)
            print("Status code: ", response.status_code)
            print("Response: ", response.json())
            msg = response.json()
            not_found = msg.get('error')
            
            if not_found:
                print("not found :", not_found)
		#lcd1.clear()
                #lcd1.cursor_pos = (0, 0)
                #lcd1.write_string('Maaf...')
                #lcd1.cursor_pos = (1, 0)
                #lcd1.write_string(not_found)
                #lcd1.cursor_pos = (2, 0)
                #sleep(4)
                #lcd1.clear()
                #lcd1.cursor_pos = (0, 0)
                #lcd1.write_string('Silahkan Tap Kartu')
                #lcd1.cursor_pos = (1, 0)
                #lcd1.write_string('Identitas Anda')
                cap.release()
                cv2.destroyAllWindows()
                
            print("error :", not_found)
            nama = msg['Nama']
            kelas = msg['Kelas']
            time = msg['Time']
            
            digit_nama = nama[:20]
            #print(digit_nama)
            #print(base64_data)
            if digit_nama:
                #displayOne(digit_nama,kelas,time)
                print("absen berhasil") 
                cap.release()
                cv2.destroyAllWindows()
            #if not_found and len(digit_nama) > 2:
            sleep(2)
            
        except Exception as error:
            if not not_found:
                #print()
                print('Mohon maaf')
                print("Absensi Gagal")
                print("Silahkan coba lagi..")
                sleep(4)
                print('Silahkan Tap Kartu')
                print('Identitas Anda')
            
            continue
        
        finally:
            cap.release()  # Move camera release outside the loop
            cv2.destroyAllWindows()
        
    else:
        print(f'Input: {user_input}')
        user_input = ''

