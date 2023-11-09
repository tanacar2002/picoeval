import os
import ipaddress
import wifi
import socketpool
import microcontroller as mc
import time

PORT = 5000
TIMEOUT = None
BACKLOG = 2
MAXBUF = 256

try:
    print("Connecting to WiFi")
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    print("Self IP", wifi.radio.ipv4_address)
    HOST = str(wifi.radio.ipv4_address)

    print("Create TCP Server socket", (HOST, PORT))
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    s.bind((HOST, PORT))
    s.listen(BACKLOG)

    buf = bytearray(MAXBUF)
    while True:
        print("Accepting connections")
        conn, addr = s.accept()
        conn.settimeout(TIMEOUT)
        print("Accepted from", addr)
        try:
            while True:
                size = conn.recv_into(buf, MAXBUF)
                print("Received", buf[:size], size, "bytes")

                conn.send(str(eval(buf[:size].decode())).encode())
                print("Sent", buf[:size], size, "bytes")
        except Exception as e:
            conn.close()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 0.1 seconds")
    time.sleep(10)
    mc.reset()
