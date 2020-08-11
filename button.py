#!/usr/bin/env python

import argparse
import configparser
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

from pyunifi.controller import Controller
from gpiozero import Button
from signal import pause

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

button2 = Button(2)
button3 = Button(3)
button4 = Button(4)

config = configparser.ConfigParser()
config.read('config.ini')

controller = config.get('config', 'controller')
username = config.get('config', 'username')
password = config.get('config', 'password')
port = config.get('config', 'port')
version = config.get('config', 'version')
siteid = config.get('config', 'siteid')
nosslverify = config.get('config', 'nosslverify')
certificate = config.get('config', 'certificate')

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--controller', default=controller)
parser.add_argument('-u', '--username', default=username)
parser.add_argument('-p', '--password', default=password)
parser.add_argument('-b', '--port', default=port)
parser.add_argument('-v', '--version', default=version)
parser.add_argument('-s', '--siteid', default=siteid)
parser.add_argument('-V', '--no-ssl-verify', default=nosslverify, action='store_true')
parser.add_argument('-C', '--certificate', default=certificate)
args = parser.parse_args()

ssl_verify = (not args.no_ssl_verify)

if ssl_verify and len(args.certificate) > 0:
        ssl_verify = args.certificate

c = Controller(args.controller, args.username, args.password, args.port, args.version, args.siteid, ssl_verify=ssl_verify)

lcd.message = 'Press button to\ngenerate voucher'

def generate_guest():
    voucher = c.create_voucher(1, 1, 480, note="unipi guest")
    code = voucher[0].get('code')

    def format_code(string):
        length_string = len(string)
        first_length = round(length_string / 2)
        first_half = string[0:first_length].lower()
        second_half = string[first_length:].upper()
        return first_half + '-' + second_half

    voucher_code = format_code(code)
    print(voucher_code)

    lcd.clear()

    lcd.message = 'Guest voucher\n{}'.format(voucher_code)

def generate_customer():
    voucher = c.create_voucher(1, 1, 5, up_bandwidth=512, down_bandwidth=512, byte_quota=1024, note="unipi customer")
    code = voucher[0].get('code')

    def format_code(string):
        length_string = len(string)
        first_length = round(length_string / 2)
        first_half = string[0:first_length].lower()
        second_half = string[first_length:].upper()
        return first_half + '-' + second_half

    voucher_code = format_code(code)
    print(voucher_code)

    lcd.clear()

    lcd.message = 'Customer voucher\n{}'.format(voucher_code)

def generate_clear():
    if button4.is_pressed:
        lcd.clear()
        lcd.message = 'Press button to\ngenerate voucher'

button2.when_pressed = generate_guest
button3.when_pressed = generate_customer
button4.when_pressed = generate_clear

pause()
