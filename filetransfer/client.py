# Import socket module
import socket
import logging
import hashlib
import time
from _thread import *
from threading import Thread
import random


msgFromClient = 'Hello UDP Server'

bytesToSend = str.encode(msgFromClient)

size = 128

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

    host = socket.gethostname()
    #host = '18.209.223.196'

    # Define the port on which you want to connect
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Connect to server on local computer
    s.sendto(bytesToSend, (host, port))

    print("Conexión con el host: ", host,
          " fue satisfactoria en el puerto: ", port)
    print("Cliente #", cliente_num, " listo")
    logging.info("CLIENT: client #%d ready", cliente_num)
    dataTotal = b''

    start_time = time.time()
    ghost = True
    f = open("prueba.txt", 'wb')

    while True:
        # Message received from server
        data, address = s.recvfrom(size)
        f.write(data)
        dataTotal += data

        if data and ghost:
            start_time = time.time()
            ghost = False
        if not data:
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
            else:
                print("Hash incorrecto")
                logging.info("CLIENT: hash corrupto")

    logging.info('CLIENT: Cantidad bytes recibidos %s', len(dataTotal))
    logging.info('CLIENT: Cantidad paquetes %s', len(dataTotal)/size)
    logging.info('CLIENT: Tiempo del envío %s', (time.time()-start_time))
    logging.info("---------------------------------------------")
    s.close()


main()
