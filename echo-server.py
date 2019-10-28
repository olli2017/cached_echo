#!/usr/bin/env python3

import os
import socket
import redis

HOST = ""  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

prefix = 'Ok:'


def cached(data):
    cache = redis.Redis(host='rediska', port=6379)
    cache.ping()
    if cache.exists(data):
        return True
    else:
        cache.set(data, data)
        return False


def sendMsg(conn, message):
    conn.sendall(message.encode('utf-8'))


def sendData(conn, message, data):
    conn.sendall(message.encode('utf-8') + data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)

            if not data:
                print('Got:', data)
                sendMsg(conn, 'Bye')
                break
            if cached(data):
                sendData(conn, 'Cached:', data)
            else:
                print('Got:', data)
                sendData(conn, prefix, data)
