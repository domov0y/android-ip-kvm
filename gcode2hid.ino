#include <EasyHID.h>
  

int cmd[4] = {0};
int index = -1;      // -1 означает "нет активного параметра"
int minus = 1;

void execGcode() {
    // Применяем знак к последнему параметру, если он был начат
    if (index >= 0) {
        cmd[index] *= minus;
        minus = 1;
    }

    int G = cmd[0], S = cmd[1], X = cmd[2], Y = cmd[3];
    switch(G) {
        case 1: Keyboard.press(S); break;
        case 2: Keyboard.release(S); break; 
        case 11: Mouse.move(X, Y); break; 
        case 12: Mouse.press(S); break; 
        case 13: Mouse.releaseAll(); break; 
    }

    // Сброс всего состояния
    memset(cmd, 0, sizeof(cmd));
    index = -1;
    minus = 1;
}

void startParam(int newIndex) {
    if (index >= 0) {
        cmd[index] *= minus;  // завершаем предыдущий параметр
    }
    minus = 1;                // сбрасываем знак для нового параметра
    index = newIndex;
    cmd[index] = 0;           // начинаем новое число с нуля
}

void setup()
{
Serial.begin(115200);
HID.begin();      
}

void loop() {
    while (Serial.available()) {
        char c = Serial.read();

        if (c >= '0' && c <= '9') {
            if (index < 0) {
                // Цифра без буквы — игнорируем или ошибка
                continue;
            }
            cmd[index] = cmd[index] * 10 + (c - '0');
        } else {
            switch(c) {
                case 'Q': startParam(0); break;
                case 'S': startParam(1); break;
                case 'X': startParam(2); break;
                case 'Y': startParam(3); break;
                case '-':  if (index >= 0 && cmd[index] == 0) { minus = -1;} break;
                case 13:
                case 10:
                    execGcode();
                    break;
                default: break;
            }
        }
    }
   HID.tick();  
}
