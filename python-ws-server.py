import json
import threading
from websocket_server import WebsocketServer
from usbserial4a import serial4a

# --- КОНФИГУРАЦИЯ ---
ARDUINO_VID = 0x2341
ARDUINO_PID = 0x0043
BAUDRATE = 9600
WS_PORT = 5000

serial_conn = None

def connect_arduino():
    global serial_conn
    try:
        serial_conn = serial4a.get_serial_port(ARDUINO_VID, ARDUINO_PID, BAUDRATE)
        if serial_conn:
            print("Arduino Connected")
            return True
    except Exception as e:
        print(f"USB Error: {e}")
    return False

def write_to_arduino(message):
    if serial_conn and serial_conn.is_open():
        try:
            serial_conn.write((message + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Write Error: {e}")

# --- ОБРАБОТЧИК WS ---
def new_client(client, server):
    print(f"New client connected: {client['id']}")

def message_received(client, server, message):
    try:
        data = json.loads(message)
        cmd = ""
        if data['type'] == 'K':
            cmd = f"K:{data['code']}:{data['state']}"
        elif data['type'] == 'M':
            cmd = f"M:{data['x']}:{data['y']}"
        elif data['type'] == 'B':
            cmd = f"B:{data['btn']}:{data['state']}"
        
        if cmd:
            write_to_arduino(cmd)
    except Exception as e:
        print(f"Parse Error: {e}")

def run_ws_server():
    server = WebsocketServer(port=WS_PORT, host='0.0.0.0')
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(message_received)
    print(f"WS Server started on port {WS_PORT}")
    server.run_forever()

if __name__ == '__main__':
    if connect_arduino():
        # WebSocket сервер должен работать в потоке
        ws_thread = threading.Thread(target=run_ws_server)
        ws_thread.daemon = True
        ws_thread.start()
        
        try:
            while True: pass
        except KeyboardInterrupt:
            print("Stop")
            if serial_conn: serial_conn.close()
    else:
        print("Arduino not found")
