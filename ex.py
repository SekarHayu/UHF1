from gpiozero import LED, Button, Buzzer
import serial

led1 = LED(17)
sw1 = Button(21)
sw2 = Button(16)
sw3 = Button(20)
buzzer = Buzzer(26)

serialPort = serial.Serial("/dev/tty0", 57600, timeout=0.5)

def sw1Pressed():
    serialPort.write("SW1 Pressed".encode('utf-8'))

def sw2Pressed():
    serialPort.write("SW2 Pressed".encode('utf-8'))

def sw3Pressed():
    serialPort.write("SW3 Pressed".encode('utf-8'))

sw1.when_pressed = sw1Pressed
sw2.when_pressed = sw2Pressed
sw3.when_pressed = sw3Pressed

try:
    while True:
        command = serialPort.read_until('\0', size=None)
        commandString = command.decode('utf-8')
        if len(commandString) > 0:
            print(commandString)
            if commandString == "Button Pressed":
                led1.on()
                buzzer.beep(0.1, 0.1, 2)
                led1.off()

except KeyboardInterrupt:
    led1.off()
    buzzer.off()