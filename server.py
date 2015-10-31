#!/usr/bin/python
# -*- coding: utf-8 -*-
import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicc = {}

    def register2json(self, nombre):
        archivo = open(nombre, "w")
        datjson = json.dump(self.dicc, archivo)

    def handle(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(current)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            lineutf = (line.decode('utf-8'))
            lineutf = lineutf.split(" sip:")
            if lineutf[0] == "REGISTER":
                address = lineutf[1].split(" ")
                exp_value = address[-1].split("\r\n")
                exp_value = exp_value[0]
                address = address[0]
                if exp_value == "0":
                    del self.dicc[address]
                    self.register2json("jsonprueba")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    print(self.dicc)
                else:
                    expires = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + float(exp_value)))
                    self.dicc[address] = [self.client_address[0], expires]
                    self.register2json("jsonprueba")
                    print(self.dicc[address][1])
                    print(self.dicc)
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")


            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
