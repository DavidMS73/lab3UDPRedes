# Import socket module
import socket
import logging
import hashlib
import time
from _thread import *
from threading import Thread
import random
from threading import Timer


msgFromClient = 'Hello UDP Server, I am ready'

bytesToSendFirstMsg = str.encode(msgFromClient)

msgFromClientLast = 'Thanks, UDP Server. I finished'

bytesToSendLastMsg = str.encode(msgFromClientLast)

size = 2**15


def main():

    cliente_num = int(random.random()*100000000000000)
    # Initializes the client log
    logging.basicConfig(filename="./clientsFiles/client" + str(cliente_num) + ".log", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    print('Bienvenido')
    m = hashlib.sha256()
    start(m, cliente_num)


def start(m, cliente_num):
    msgFromClient2 = 'Archivo: '

    #host = socket.gethostname()
    host = '18.209.223.196'

    # Define the port on which you want to connect
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    s.settimeout(2)

    # Connect to server on local computer
    s.sendto(bytesToSendFirstMsg, (host, port))\


    print("Conexión con el host: ", host,
          " fue satisfactoria en el puerto: ", port)
    print("Cliente #", cliente_num, " listo")
    logging.info("CLIENT: client #%d ready", cliente_num)
    dataTotal = b''

    start_time = time.time()
    ghost = True
    f = open("prueba.txt", 'wb')
    cont = 1

    try:
        while True:
            # Message received from server
            try:
                data, address = s.recvfrom(size)
                f.write(data)
                print('receiving...', cont)
                cont = cont + 1
                dataTotal += data

                if data and ghost:
                    start_time = time.time()
                    ghost = False
                if not data:
                    print("Fin envío")
                    break
                elif (data.__contains__(b"HASHH")):
                    logging.info("Found hash")
                    index = data.find(b"HASHH")

                    index2 = dataTotal.find(b"HASHH")

                    m.update(dataTotal[:index2])

                    realM = data[index+5:]
                    print("Hash recibido ", realM.decode())
                    print("Hash creado ", m.hexdigest())
                    if m.hexdigest() == realM.decode():
                        print("Hash correcto")
                        logging.info("CLIENT: hash correcto")
                        msgFromClient2 += 'correcto'
                    else:
                        print("Hash incorrecto")
                        logging.info("CLIENT: hash corrupto")
                        msgFromClient2 += 'incorrecto'
                    s.sendto(bytesToSendLastMsg, (host, port))
            except socket.timeout:
                print('Timeout')
                msgFromClient2 = 'incorrecto'
                break

    finally:
        #bytesToSendSecondMsg = str.encode(msgFromClient2)
        #s.sendto(bytesToSendSecondMsg, (host, port))
        logging.info('CLIENT: Cantidad bytes recibidos %s', len(dataTotal))
        logging.info('CLIENT: Cantidad paquetes recibidos %s', cont)
        logging.info('CLIENT: Tiempo del envío %s', (time.time()-start_time))
        logging.info("---------------------------------------------")
        s.close()


main()
