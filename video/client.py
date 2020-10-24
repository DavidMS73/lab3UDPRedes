# import socket
# import struct
# import sys

# ack = 'ack'
# multicast_group = '18.209.223.196'
# #multicast_group = socket.gethostname()
# server_address = ('', 40000)

# # Create the socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind to the server address
# sock.bind(server_address)

# # Tell the operating system to add the socket to the multicast group
# # on all interfaces.
# group = socket.inet_aton(multicast_group)
# mreq = struct.pack('4sL', group, socket.INADDR_ANY)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# # Receive/respond loop
# while True:
#     print('\nWaiting to receive message')
#     data, address = sock.recvfrom(1024)

#     print('Received %s bytes fromm %s' % (len(data), address))
#     print(data)

#     print('Sending acknowledgement to', address)
#     sock.sendto(ack.encode("ascii"), address)




# Welcome to PyShine
# lets make the client code
# In this code client is sending video to server
import socket,cv2, pickle,struct
import pyshine as ps # pip install pyshine
import imutils # pip install imutils
import struct
# client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host_ip = '18.209.223.196' # Here according to your server ip write the address
port = 9999

#Multicast stuff
channel = int(input("Ingrese el canal a conectarse (1, 2 o 3)"))
multicast_groups = ['18.209.223.196', '18.209.223.196', '18.209.223.196']
server_address = ('', 10000)

#Bind para multicast
#client_socket.connect((host_ip,port))
# client_socket.bind(("", port ))
multicast_port  = 9999
multicast_group = "18.209.223.196"
interface_ip    = "10.11.1.43"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# mreq = inet_aton(multicast_group) + inet_aton(interface_ip)
sock.bind((multicast_group, multicast_port))
mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


# mreq = socket.inet_aton(multicast_groups[channel-1]) + socket.inet_aton(host_ip)
# group=multicast_groups[channel-1]
# mreq = struct.pack(
#             '4sI',
#             socket.inet_aton(group),
#             socket.inet_aton(host_ip))
# client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

#group = socket.inet_aton(multicast_groups[channel-1])
#mreq = struct.pack('4sL', group, socket.INADDR_ANY)
#client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

try:
    print('CLIENT {} CONNECTED!'.format(20))
    if client_socket:  # if a client socket exists
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = s.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            frame = ps.putBText(frame, f"Canal {channel}", 10, 10, vspace=10, hspace=1, font_scale=0.7,
                                 text_RGB=(255, 250, 250))
            cv2.imshow(f"FROM ", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()
except Exception as e:
    print(e)
    client_socket.close()
    print(f"CLIENT DISCONNECTED")
    pass