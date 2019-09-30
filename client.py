# coding=utf-8
import socket
import os
import subprocess
import pickle
import sys
import threading



host = str(sys.argv[1])
port = int(sys.argv[2])

s = socket.socket()
s.connect((host, port))

def downloadTCP(file):
    f = open("./uploaded/" + file, "wb")
    while True:
        print('receiving data...')
        data = s.recv(1024)
        if data == b'3nd?tr4ns':
            s.send(b'done')
            break
        f.write(data)
    print("El archivo se ha recibido correctamente.")
    f.close()


def uploadTCP(file):
    while True:
        f = open("./downloaded/" + file, "rb")
        content = f.read(1024)
        while content:
            s.send(content)
            content = f.read(1024)
        s.send(chr(1))

        f.close()
        print("El archivo ha sido enviado correctamente.")
        break

def tcpClient():
    while True:
            msg = raw_input('->')
            s.send(msg.encode())

            if msg == 'salir':
                print("Salir")

            elif msg =='-d':
                file = str(sys.argv[3])
                s.send(bytes(file.encode('utf-8')))
                downloadTCP(file)

            elif msg =='-u':
                file = str(sys.argv[3])
                s.send(bytes(file.encode('utf-8')))
                uploadTCP(file)

            elif msg == '-l':
                for x in os.listdir('..\\redesHW'):
                    if os.path.isfile(x):
                        print 'f-', x
                    elif os.path.isdir(x):
                        print 'd-', x
                        for j in os.listdir('..\\redesHW\\' + x):
                            print('\t'+j)
                    elif os.path.islink(x):
                        print 'l-', x
                    else:
                        print '---', x
            else:
                s.close()
                sys.exit()

def udpClient():
    while True:
        msg = raw_input('->')
        s.send(msg.encode())

        if msg == 'salir':
            print("Salir")

        elif msg == '-u':
            file = str(sys.argv[3])
            s.sendto(bytes(file.encode('utf-8')),(host,port))
            uploadUDP(file)

        elif msg == '-d':
            file = str(sys.argv[3])
            s.sendto(bytes(file.encode('utf-8')),(host,port))
            downloadUDP(file)

        else:
            s.close()
            sys.exit()

def uploadUDP(file):

    while True:
        f = open("./downloaded/" + file, "rb")
        content = f.read(1024)
        while content:
            s.sendto(content,(host,port))
            content = f.read(1024)
        s.sendto(chr(1),(host,port))

        f.close()
        print("El archivo ha sido enviado correctamente.")
        break

def downloadUDP(file):
    f = open("./uploaded/" + file, "wb")
    while True:
        try:
            input_data = s.recvfrom(1024)
        except:
            print("Error de lectura.")
            break
        else:
            if input_data[0]:
                # Compatibilidad con Python 3.
                if isinstance(input_data, bytes):
                    end = input_data[0] == 1
                else:
                    end = input_data[0] == chr(1)
                if not end:
                    # Almacenar datos.
                    f.write(input_data[0])
                else:
                    break

    print("El archivo se ha recibido correctamente.")
    f.close()


udpClient()