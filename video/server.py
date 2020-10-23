# import socket
# import struct
# import sys

# message = 'message in multicast'
# multicast_group = ('18.209.223.196', 40000)
# #multicast_group = (socket.gethostname(), 40000)

# # Create the datagram socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Set a timeout so the socket does not block indefinitely when trying
# # to receive data.
# sock.settimeout(20)

# # Set the time-to-live for messages to 1 to they do not go past the
# # local network segment.
# ttl = struct.pack('b', 1)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


# try:

#     # Send data to the multicast group
#     print('Enviando "%s"' % message)

#     sent = sock.sendto(message.encode("ascii"), multicast_group)

#     while True:
#         print('Esperando respuesta')
#         try:
#             data, server = sock.recvfrom(16)
#         except socket.timeout:
#             print('timed out, no se recibieron mas respuestas')
#             break
#         else:
#             print('Recibido "%s" de %s' % (data, server))

# finally:
#     print('Socket cerrado')
#     sock.close()




# Welcome to PyShine
# In this video server is receiving video from clients.
# Lets import the libraries
import socket, cv2, pickle, struct
import imutils
import threading
import pyshine as ps  # pip install pyshine
import cv2
vid = cv2.VideoCapture('./data/Redes5G.mp4')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Multicast Stuff
multicast_group = ('18.209.223.196', 10000)
ttl = struct.pack('b', 1)
#server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)


def show_client(addr, client_socket):
    if client_socket:
        while (vid.isOpened()):
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame, width=380)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendto(message,multicast_group)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    client_socket.close()
            except Exception as e:
                client_socket.close()
                print(f'VIDEO FINISHED! to client {addr}')
                break



while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()
    print("TOTAL CLIENTS ", threading.activeCount() - 1)