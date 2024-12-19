import RPi.GPIO as GPIO
import serial
import crcmod
import time
import cv2
import base64
import numpy as np
import requests
from time import sleep
import aiohttp
import asyncio

'''
https://10.42.0.232/api/system/gate/status (get json)
https://10.42.0.232/api/system/gateone/open/boolean (switch auto/man gate 1)
https://10.42.0.232/api/system/gatetwo/open/boolean (switch auto/man gate 2)
'''
master_control = 23
gate_up = 24
gate_down = 25
gate_open_close_man = 26
relay_vld = 8

GPIO.setmode(GPIO.BCM)  # Atur mode pin berdasarkan nomor fisik
#GPIO.setup(relay_vld, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Inisialisasi pin dengan pull down
GPIO.setup(gate_up,GPIO.OUT)
GPIO.setup(gate_down,GPIO.OUT)
GPIO.setup(gate_open_close_man,GPIO.OUT)
GPIO.setup(master_control,GPIO.OUT)
GPIO.setup(relay_vld,GPIO.IN)

data_list = []
found_07 = False
cache = ''
# Buat objek serial dengan baudrate 115200
ser = serial.Serial('/dev/ttyUSB0', 57600)
#print(ser.read())
# Buat fungsi untuk menghitung CRC-16
crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)

# Buat fungsi untuk mengirim perintah ke perangkat
def send_command(cmd):
    # Tambahkan header, tipe, dan panjang data
    frame = b'\xBB' + cmd[0:2] + bytes([len(cmd) - 2])
    # Tambahkan data
    frame += cmd[2:]
    # Hitung dan tambahkan CRC-16
    crc = crc16(frame)
    frame += bytes([crc & 0xFF, crc >> 8])
    # Tambahkan end byte
    frame += b'\x7E'
    # Kirim frame ke perangkat
    ser.write(frame)

# Buat fungsi untuk menerima respon dari perangkat
def receive_response():
    # Baca byte pertama dari perangkat
    global data_list, found_07, cache
    byte = ser.read()
    #print(byte)
    data2 = ser.read(16)

    if data2.hex() != '00':
        data_list.append(data2.hex())
        data_list = data_list[-8:]
    if byte == b'\x07':
        tipe = ser.read()
        panjang = ser.read()
        data = ser.read(ord(panjang))
        crc = ser.read(2)
        end = ser.read()
        return (tipe, data)
    
    return None


async def send_request(url, body):
    
    print("Requests api sedang diproses")
    response = requests.post(url, data=body)
    print("url :", url)
    print("Status code: ", response.status_code)
    print("Response: ", response.json())
    print("SUCCES SAVE IMAGE AS Base64")
    

async def send_state(url, state):
    #print("Requests api sedang diproses")
    response = requests.get(url+state)
 
        
# Buat fungsi untuk membaca data RFID secara terus menerus
async def read_rfid():
    
    send_command(b'\0x01')
    print("Program sedang berjalan ")
    GPIO.output(master_control, True)
    cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
    
    while True:
        
        input_state = GPIO.input(relay_vld)
        send_command(b'\0x02')
        respon = receive_response()
        data = requests.get('http://192.168.49.37:1000/api/system/gate/status') 
        # Mengekstrak nilai dari 'StateGate_1' dan 'isAuto'
        gate_status = data.json().get('StateGate_1', {})
        is_auto = gate_status.get('isAuto', None)
        is_open = gate_status.get('isOpen', None)
        
        if respon is not None:
            
            GPIO.output(gate_up, True)
            GPIO.output(gate_down, False)
            await send_state('https://10.42.0.232/api/system/gateone/open/', 'true')
            uid = respon[1][4:12]
            uid_to_hex = uid.hex()
            print(uid.hex())
            with open('exit.txt', 'r') as f:
                data = f.read()
            
            if is_auto == True:
                
                GPIO.output(master_control, True)
                
            if is_auto == False:
                
                GPIO.output(master_control, False)
                
            if is_open == True and is_auto == True:
                
                GPIO.output(gate_up, True)
                GPIO.output(gate_down, False)
            
            if is_open == False and is_auto == True:
                
                GPIO.output(gate_up, False)
                GPIO.output(gate_down, True)
            
            if uid.hex() and is_auto == True:
                try:
                    with open('enter.txt', 'w') as f:
                        f.write('ENTER')
                    for _ in range(26):  # discard the first 10 frames
                        _, _ = cap.read()
                    ret, image = cap.read()
                    alpha = 1  # Faktor kontrast
                    beta = 2    # Faktor kecerahan
                    brightened_frame = cv2.addWeighted(image, alpha, image, 0, beta)
                    ret, buffer = cv2.imencode('.jpg', brightened_frame)
                    jpg_as_text = base64.b64encode(buffer).decode()
                    url = f"https://10.42.0.232/enter/{uid_to_hex}"
                    body = {
                            "capture": jpg_as_text
                           }
                    
                    await send_request(url, body)
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    sleep(3)
                    GPIO.output(gate_up, False)
                    GPIO.output(gate_down, True)
                    await send_state('https://10.42.0.232/api/system/gateone/open/', 'false')
                    GPIO.cleanup()

                    '''
                    async with aiohttp.ClientSession() as session:
                        async with session.post(url, data=body) as response:
                            print("url :", url)
                            print("Status code: ", response.status)
                            print("Response: ", await response.json())
                            print("SUCCES SAVE IMAGE AS Base64")
                    '''
                    
                except Exception as e:
                    print("terjadi kesalahan", e)
                    continue
                
    cap.release()
    cv2.destroyAllWindows()

# Jalankan fungsi dengan event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(read_rfid())
loop.close()