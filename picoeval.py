#!/usr/bin/env python3

import sys
import time
import serial
import socket

HOST = "192.168.248.55"
PORT = 5000 

args = sys.argv

print("....................hi....")

if len(args) == 1 or (len(args) == 2 and args[-1] == "s"):
    print("You need to supply an expression")
    print("....................bye...")
    raise KeyError

if args[-1] == "w":
    client_socket = socket.socket()  # instantiate
    client_socket.connect((HOST, PORT))  # connect to the server
    for exp in args[1:-1]:
        client_socket.send(exp.encode())
        data = client_socket.recv(256).decode()  # receive response

        print(data)  # show in terminal
else:
    ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)
    #print("Connected")
    time.sleep(0.1)
    data = b'a'
    while data != b'\\':
            data = ser.read()

    if args[-1] == "s":
        args = args[:-1]

    for exp in args[1:]:
        ser.write(f"{exp}\r".encode()) #send input
        data = ser.read_until(b'>>> ')
        if len(data):
            #print(data)
            print(int(data.split(b"\r\n")[1]))
print("....................bye...")
