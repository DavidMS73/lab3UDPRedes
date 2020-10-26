# Import socket programming library
import socket

# Import thread module
from _thread import *
import threading
import logging
import hashlib
import time
from threading import Thread

size = 2**15


# Thread function
# Socket is the socket object with which connection was made, used to send and receive messages
def threaded(socketServer, address, threadNum):

    m = hashlib.sha256()

    logging.info("SERVER thread #%s: iniciando", threadNum)
    print("SERVER thread #", threadNum,
          ". El archivo que se va a abrir es: ", file)

    logging.info("SERVER thread #%s: el archivo abierto fue %s ",
                 threadNum, file)

    start_time = time.time()

    fileHash = open(file, "rb")
    dataHash = fileHash.read()
    m.update(dataHash)
    h = m.hexdigest()
    print("Digest enviado: ", h)
    fileHash.close()

    f = open(file, "rb")
    data = f.read(size)
    numBytes = 0
    while (data):
        rta = socketServer.sendto(data, address)

        if(rta):
            numBytes += rta
            data = f.read(size)
    f.close()

    numBytesHash = socketServer.sendto(("HASHH" + h).encode(), address)

    # logging.info('SERVER thread #%s: bytes enviados sin hash %s',
    #              threadNum, numBytes)

    # logging.info('SERVER thread #%s: bytes enviados en total %s',
    #              threadNum, numBytes + numBytesHash)

    # with open(file, 'rb') as f:

    #     # File
    #     data = f.read()

    #     m.update(data)
    #     start_time = time.time()
    #     # Send back reversed string to client
    #     numBytes = socket.sendto(data, address)

    #     print("Fin de envío thread #", threadNum)

    #     # Send hash
    #     h = m.hexdigest()
    #     print("Digest enviado: ", h)
    #     numBytesHash = socket.sendto(("HASHH" + h).encode(), address)

    #     logging.info('SERVER thread #%s: bytes enviados sin hash %s',
    #                  threadNum, numBytes)

    #     logging.info('SERVER thread #%s: bytes enviados en total %s',
    #                  threadNum, numBytes + numBytesHash)

    logging.info('SERVER thread #%s: tiempo del envío %s', threadNum,
                 (time.time()-start_time))

    # bandera = True

    # while(True and bandera):
    #     data, address = socketServer.recvfrom(size)
    #     if (data):
    #         bandera = False

    # logging.info("SERVER thread #%s. Cliente: ", data)
    # print("SERVER thread #", threadNum, ". Cliente: ", data)


def main():
    logging.basicConfig(filename="./serverFiles/serverLog.log", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )

    global file

    # Initializes the server log
    host = socket.gethostname()
    # Port number
    port = 50000
    logging.info('Connected to %s on port %s', host, port)

    # Socket del servidor
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind((host, port))
    print('Port: ', port)

    # Become a server socket
    print("Socket listening")
    inputText = int(input("\n ¿Qué archivo desea enviar?"
                          "\n 1. 145 MB - Multimedia"
                          "\n 2. 355 MB - Multimedia"
                          "\n 3. 200 MB - Archivo\n"))
    if inputText == 1:
        f = "./data/Redes5G.mp4"
    elif inputText == 2:
        f = "./data/Vivaldi.mp4"
    else:
        f = "./data/200MB.zip"

    file = f
    print("Archivo seleccionado: ", file)
    global num_conn
    num_conn = int(
        input('\n ¿A partir de cuántas conexiones desea enviar? \n'))
    logging.info('SERVER: el número de conexiones definido es %s', num_conn)
    print("Esperando conexiones...")

    # Threads connect
    threads = []
    while True:
        # Accept connections from outside
        data, address = serversocket.recvfrom(size)
        # lock acquired by client
        # print_lock.acquire()
        print('Mensaje recibido: ', data)
        if not data.__contains__(b'Thanks, UDP Server. I finished'):
            print('Connected to: ', address[0], ':', address[1])
            logging.info('Message received from client: ' + str(data) +
                        '. IP: ' + str(address[0]) + ', port: ' + str(address[1]))

            t = Thread(target=threaded, args=(serversocket, address, len(threads)))
            threads.append(t)

            if len(threads) == num_conn:
                for i in threads:
                    i.start()
                threads = []
                logging.info('SERVER: reiniciando threads')

    serversocket.close()


main()
