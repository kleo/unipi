#!/usr/bin/env python

import argparse
import configparser
import board
import time
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import os

from pyunifi.controller import Controller
from gpiozero import Button
from gpiozero import OutputDevice

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
reset = Button(3,bounce_time=5)
coinslotpower = OutputDevice(4)

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
    
# https://stackoverflow.com/questions/52126586/python-scripting-for-coins-slot-raspberry-pi
while True:
    total = 0
    state = True
    counter = 0
    lcd.clear()
    lcd.message = 'Insert coin and\npress confirm'
    while state:
        if coinslot.is_pressed:
            counter+=1
            time.sleep(.05)
            lcd.clear() 
            
            if counter == 1:
                lcd.message = '{} Peso\ninserted'.format(counter)
            else:
                lcd.message = '{} Pesos\ninserted'.format(counter)

        # https://gist.github.com/alaudet/9e280d190bff83830dc7
        if reset.is_pressed:
            time.sleep(5)
            if reset.is_pressed:
                    lcd.clear()
                    lcd.message = "Shutting down"

                    cmd = "sudo shutdown -h now"
                    os.system(cmd)

        if confirm.is_pressed:
            state = False
            total = counter * 4 # 1 peso = 4 minutes

            if total == 0:
                lcd.clear()
                lcd.message = 'No coin inserted\nplease wait'
                coinslotpower.off()
                time.sleep(5)
                coinslotpower.on()
                break

            def generate_guest():
                voucher = c.create_voucher(1, 1, total, up_bandwidth=4098, down_bandwidth=4098, note="unipi guest") # remove quota
                code = voucher[0].get('code')

                def format_code(string):
                    length_string = len(string)
                    first_length = round(length_string / 2)
                    first_half = string[0:first_length].lower()
                    second_half = string[first_length:].upper()
                    return first_half + '-' + second_half

                voucher_code = format_code(code)

                lcd.clear()
                # https://stackoverflow.com/a/18175488/10025507
                timeout = 90
                while timeout != 0:
                    if reset.is_pressed:
                        break
                
                    lcd.message = 'Guest voucher {:2d}\n{}'.format(timeout, voucher_code)
                    time.sleep(1)
                    timeout = timeout-1

            generate_guest()
