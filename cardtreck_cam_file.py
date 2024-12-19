# Import library yang diperlukan
import serial
import crcmod
import time

import cv2


data_list = []
found_07 = False

# Buat objek serial dengan baudrate 115200
ser = serial.Serial('/dev/ttyUSB0', 57600)

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
    global data_list, found_07
    byte = ser.read()
    #print(byte)
    data2 = ser.read(16)
    #print("Data ", data2.hex())
    if data2.hex() != '00':
        data_list.append(data2.hex())
        data_list = data_list[-8:]
    #found_07 = False
    # Gabungkan hasil pembacaan byte menjadi satu nilai yang lengkap
    #print(data_list)
    # Jika byte pertama adalah header
    if byte == b'\x07':
        # Baca tipe dan panjang data
        tipe = ser.read()
        panjang = ser.read()
        # Baca data sesuai panjang
        data = ser.read(ord(panjang))
        # Baca CRC-16 dan end byte
        crc = ser.read(2)
        end = ser.read()
        #print("Data : ",crc, end)
        # Jika end byte adalah 0x7E
        #if end == b'\x7E':
        # Kembalikan tipe dan data sebagai tuple
        #print("tipe data : ", data.decode("latin-1"))
        return (tipe, data)
    # Jika tidak ada respon yang valid, kembalikan None
    return None

# Buat fungsi untuk menampilkan data RFID dalam format hex
def print_hex(data):
    # Untuk setiap byte dalam data
    for byte in data:
        # Cetak byte dalam format hex dengan padding 0
        print('{:02X}'.format(byte), end=' ')
    # Cetak baris baru
    print()

# Buat fungsi untuk membaca data RFID secara terus menerus
def read_rfid():
    # Kirim perintah untuk mengaktifkan mode inventory
    send_command(b'\0x01')
    # Tunggu 0.1 detik
    time.sleep(0.1)
    
    # Ulangi selamanya
    while True:
        
        # Kirim perintah untuk membaca data RFID
        cap = cv2.VideoCapture(3, cv2.CAP_V4L2)
        #cv2.imshow('uid', image)
        send_command(b'\0x02')
        
        # Tunggu 0.1 detik
        time.sleep(0.1)
        # Menerima respon dari perangkat
        respon = receive_response()
        # Jika ada respon yang valid
        
        if respon is not None:
            #print("respon :",respon[1][4:8])
            uid = respon[1][4:8]
            print(uid.hex())
            if uid.hex():
                for _ in range(26):  # discard the first 10 frames
                    _, _ = cap.read()
                ret, image = cap.read()

                alpha = 1  # Faktor kontrast
                beta = 2    # Faktor kecerahan
                brightened_frame = cv2.addWeighted(image, alpha, image, 0, beta)

                #cv2.imshow("captured_image_brightened", brightened_frame)
                cv2.imwrite(f"{uid.hex()}.jpg", brightened_frame)

                cap.release()
                cv2.destroyAllWindows()
                print("saved image")
            # Jika tipe respon adalah 0x01 (respon dari perangkat)
            if respon[0] == b'\x00':
                # Jika data respon berisi UID RFID
                if respon[1][0] == 0 and respon[1][1] == 147:
                    # Ambil UID RFID dari data respon
                    uid = respon[1][4:8]
                    # Tampilkan UID RFID dalam format hex
                    
        # Tunggu 0.1 detik
        time.sleep(0.1)
        cap.release()
        cv2.destroyAllWindows()

# Panggil fungsi untuk membaca data RFID
read_rfid()
