#!/usr/bin/env python

import argparse
import configparser
import board
import time
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

from pyunifi.controller import Controller
from gpiozero import Button

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

coinslot = Button(17)
confirm = Button(2,bounce_time=5)

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
    
while True:
    total = 0
    coinslotState = True
    counter = 0
    lcd.message = 'Insert coin and\npress confirm'
    print(f'total: {total}, counter: {counter}, state: {coinslotState}')
    while coinslotState:
        if coinslot.is_pressed:
            counter+=1
            time.sleep(.05)
            print(counter)
            lcd.clear()
            lcd.message = '{} Pesos\ninserted'.format(counter)
            
        if confirm.is_pressed:
            coinslotState = False

            total = counter * 5
            print(f'total: {total}, counter: {counter}, state: {coinslotState}')

            def generate_guest():
                cvou = c.create_voucher(1, 1, total, note="unipi guest")
                vou = cvou[0].get('code')

                def format_code(string):
                    length_string = len(string)
                    first_length = round(length_string / 2)
                    first_half = string[0:first_length].lower()
                    second_half = string[first_length:].upper()
                    return first_half + '-' + second_half

                pvou = format_code(vou)
                print(pvou)

                lcd.clear()

                lcd.message = 'Guest voucher\n{}'.format(pvou)
                time.sleep(60)
                
            generate_guest()
            