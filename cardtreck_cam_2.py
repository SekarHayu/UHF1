import multiprocessing
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

data_list = []
found_07 = False
cache = ''
data = ''
ser = serial.Serial('/dev/ttyUSB0', 57600)
crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)

# Membuat lock
lock = multiprocessing.Lock()

def send_command(cmd):
    frame = b'\xBB' + cmd[0:2] + bytes([len(cmd) - 2])
    
    frame += cmd[2:]
    
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
    with open('exit.txt', 'w') as f:
        f.write('')

# Buat fungsi untuk membaca data RFID secara terus menerus
async def read_rfid():
    global data
    send_command(b'\0x01')
    print("Program sedang berjalan ")
    
    while True:
        send_command(b'\0x02')
        respon = receive_response()
        if respon is not None:
            # Menggunakan lock saat mengakses kamera
            lock.acquire()
            try:
                cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
                uid = respon[1][4:12]
                uid_to_hex = uid.hex()
                print(uid.hex())
                with open('enter.txt', 'r') as f:
                    data = f.read()
                if uid.hex() and  data != "ENTER":
                    try:
                        with open('exit.txt', 'w') as f:
                            f.write('EXIT')
                        for _ in range(26):  # discard the first 10 frames
                            _, _ = cap.read()
                        ret, image = cap.read()
                        alpha = 1  # Faktor kontrast
                        beta = 2    # Faktor kecerahan
                        brightened_frame = cv2.addWeighted(image, alpha, image, 0, beta)
                        ret, buffer = cv2.imencode('.jpg', brightened_frame)
                        jpg_as_text = base64.b64encode(buffer).decode()
                        url = f"https://api.tierkun.my.id/enter/{uid_to_hex}"
                        body = {
                                "capture": jpg_as_text
                               }
                        
                        await send_request(url, body)
                        cap.release()
                        cv2.destroyAllWindows()
                    except Exception as e:
                        print("terjadi kesalahan", e)
                        continue
            finally:
                # Melepaskan lock setelah selesai menggunakan kamera
                lock.release()
    cap.release()
    cv2.destroyAllWindows()
loop = asyncio.get_event_loop()
loop.run_until_complete(read_rfid())
loop.close()
