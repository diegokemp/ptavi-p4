#!/usr/bin/python
# -*- coding: utf-8 -*-
import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicc = {}

    def handle(self):
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
                #print(exp_value)
                if exp_value == "0":
                    del self.dicc[address]#BORRAR
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    print(self.dicc)
                else:
                    self.dicc[address] = [self.client_address[0]]#AÑADIR
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
