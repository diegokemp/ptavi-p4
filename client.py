#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
IP = sys.argv[1]
PUERTO = int(sys.argv[2])
LINEA = sys.argv[3:]
if LINEA[0] == "register":
    mensaje = "REGISTER sip:" + LINEA[1] + " SIP/2.0\r\n\r\n"
else:
    mensaje = " ".join(LINEA)

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PUERTO))

print("Enviando: " + mensaje)
my_socket.send(bytes(mensaje, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
