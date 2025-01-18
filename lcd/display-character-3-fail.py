from RPLCD.gpio import CharLCD
import lgpio

#chip = gpiod.Chip("/dev/gpiochip0")
h = lgpio.gpiochip_open(0)


# Initialize the LCD using lgpio
lcd = CharLCD(
    cols=16, rows=2, pin_rs=27, pin_e=17, pins_data=[25,24,23,22],
    numbering_mode=CharLCD.BCM, gpio_chip=h
              )

lcd.clear()
# Write a message
lcd.write_string("Hello, World!")
lcd.cursor_pos = (1,0)
lcd.write_string("Sunjoo Park")
# Clean up after use
#lcd.close()

lgpio.gpiochip_close(h)
