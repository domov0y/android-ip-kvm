#!/usr/bin/env python3
# простой тест для скетча посылающего hid  команды  в usb. требует проверки. впрочем как и сам скетч ардуино. 
import sys
import time
import serial

PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
DELAY = 0.01


if len(sys.argv) != 2:
    print(f"Использование: {sys.argv[0]} commands.txt")
    sys.exit(1)


with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    time.sleep(2)  # Arduino может перезагрузиться при открытии порта

    with open(sys.argv[1], "r") as f:
        for line in f:
            line = line.strip()

            # пустые строки и комментарии пропускаем
            if not line or line.startswith(";") or line.startswith("#"):
                continue

            print(">", line)

            ser.write((line + "\n").encode())
            ser.flush()

            time.sleep(DELAY)
