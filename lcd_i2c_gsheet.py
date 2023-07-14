import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurasi LCD 16x2 dengan modul I2C
lcd_columns = 16
lcd_rows = 2
lcd_address = 0x27  # Alamat I2C LCD, dapat berbeda tergantung pada modul yang Anda gunakan
lcd_backlight = 0x08  # Atur nilai ini menjadi 0x00 jika Anda tidak ingin menyalakan pencahayaan latar LCD

# Inisialisasi SMBus
bus = smbus.SMBus(1)  # Gunakan 0 jika menggunakan Raspberry Pi model lama

# Fungsi untuk mengirim data ke LCD melalui I2C
def lcd_byte(data, mode):
    # Mengirim byte tinggi
    bus.write_byte(lcd_address, mode | (data & 0xF0) | lcd_backlight)
    # Mengirim byte rendah
    bus.write_byte(lcd_address, mode | ((data << 4) & 0xF0) | lcd_backlight)
    time.sleep(0.0001)  # Tunggu sebentar

# Fungsi untuk mengirim perintah ke LCD
def lcd_command(cmd):
    lcd_byte(cmd, 0x00)

# Fungsi untuk menampilkan karakter di LCD
def lcd_character(char):
    lcd_byte(ord(char), 0x01)

# Fungsi untuk mengirim string ke LCD
def lcd_string(message):
    for char in message:
        lcd_character(char)

# Konfigurasi Google Sheets
spreadsheet_id = 'YOUR_SPREADSHEET_ID'  # Ganti dengan ID spreadsheet Anda
sheet_name = 'Sheet1'  # Ganti dengan nama sheet Anda

# Mengatur kredensial OAuth 2.0
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', ['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(credentials)

# Membuka spreadsheet dan sheet
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.worksheet(sheet_name)

# Inisialisasi LCD
lcd_command(0x33)
lcd_command(0x32)
lcd_command(0x28)  # Mode 2 baris
lcd_command(0x0C)  # Tampilkan kursor tanpa kedipan
lcd_command(0x06)  # Geser kursor ke kanan
lcd_command(0x01)  # Bersihkan layar

while True:
    try:
        # Membaca data input dari Google Sheets
        data = sheet.col_values(2)[-1]  # Membaca data dari kolom B, baris terakhir

        # Tampilkan data di LCD
        lcd_command(0x80)  # Pindah ke baris pertama
        lcd_string('Data Input:')
        lcd_command(0xC0)  # Pindah ke baris kedua
        lcd_string(data)

        time.sleep(2)  # Tunggu selama 2 detik sebelum membaca data berikutnya
    
    except Exception as e:
        # Tangani jika terjadi kesalahan saat membaca data
        print('Error reading data:', str(e))
        time.sleep(2)
        continue

