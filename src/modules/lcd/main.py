# -*- coding: utf-8 -*-
import time


def lcd_driver(lcd_quee):
    while True:
        print('lcd_driver')
        time.sleep(1)


if __name__ == '__main__':
    lcd_driver()