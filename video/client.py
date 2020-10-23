import socket
import struct
import sys

ack = 'ack'
multicast_group = '18.209.223.196'
#multicast_group = socket.gethostname()
server_address = ('', 40000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print('\nWaiting to receive message')
    data, address = sock.recvfrom(1024)

    print('Received %s bytes fromm %s' % (len(data), address))
    print(data)

    print('Sending acknowledgement to', address)
    sock.sendto(ack.encode("ascii"), address)