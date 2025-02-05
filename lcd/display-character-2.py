from RPLCD.gpio import CharLCD
from RPi import GPIO
from datetime import datetime
import time
GPIO.setmode(GPIO.BCM)
# Initialize the LCD using lgpio
lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=27, pin_e=17, pins_data=[25,24,23,22])
# Write a message
#lcd.write_string("welcome, sunjoo")
while True:
    lcd.clear()
    now = datetime.now()
    date_str = str(now.strftime("%D"))
    time_str = str(now.strftime("%T"))
    lcd.cursor_pos = (0,0)
    lcd.write_string("Date: " + date_str)
    lcd.cursor_pos = (1,0)
    lcd.write_string("Time: " + time_str)
    time.sleep(2)
lcd.close()
#GPIO.cleanup()
# Clean up after use
