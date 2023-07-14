import time
import board
import adafruit_dht
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Inisialisasi sensor DHT11
dht_device = adafruit_dht.DHT11(board.D2)

# Inisialisasi LCD 16x2 dengan modul I2C
lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

while True:
    try:
        # Baca data suhu dan kelembaban dari sensor DHT11
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        
        # Tampilkan data di LCD
        lcd.clear()
        lcd.message('Suhu: {0:.1f} C\n'.format(temperature_c))
        lcd.message('Kelembaban: {0:.1f} %'.format(humidity))
        
        time.sleep(2)  # Tunggu selama 2 detik sebelum membaca data berikutnya
    
    except RuntimeError as e:
        # Tangani jika ada error saat membaca sensor
        print('Error reading DHT sensor:', e.args[0])
        time.sleep(2)
        continue
