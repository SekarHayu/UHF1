from RPLCD.i2c import CharLCD

# Membuat instance LCD
'''lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
               cols=16, rows=2, dotsize=8,
               charmap='A02',
               auto_linebreaks=True,
               backlight_enabled=True)
               '''
lcd2 = CharLCD(i2c_expander='PCF8574', address=0x27, port=4
               ,
               cols=16, rows=2, dotsize=8,
               charmap='A02',
               auto_linebreaks=True,
               backlight_enabled=True)

# Menulis teks ke setiap LCD
#lcd1.write_string('Hello LCD 1')
lcd2.write_string('Hello LCD 2')
