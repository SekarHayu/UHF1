import RPi.GPIO as GPIO
import time

master_control = 26
gate_up = 24
gate_down = 25
relay_vld = 8
remote = 23

GPIO.setmode(GPIO.BCM)  # Atur mode pin berdasarkan nomor fisik
#GPIO.setup(relay_vld, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Inisialisasi pin dengan pull down
GPIO.setup(gate_up,GPIO.OUT)
GPIO.setup(gate_down,GPIO.OUT)
GPIO.setup(remote,GPIO.OUT)
GPIO.setup(master_control,GPIO.OUT)
GPIO.setup(relay_vld, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    vld = GPIO.input(relay_vld)
    time.sleep(1)
    print(vld)
    GPIO.setwarnings(False)
    GPIO.output(master_control, False)
    GPIO.output(remote, False)
    GPIO.output(gate_down, True)
    #GPIO.output(gate_down, True)
GPIO.cleanUp()