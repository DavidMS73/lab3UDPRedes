import socket
import struct
import sys

message = 'message in multicast'
multicast_group = ('18.209.223.196', 40000)
#multicast_group = (socket.gethostname(), 40000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(20)

# Set the time-to-live for messages to 1 to they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


try:

    # Send data to the multicast group
    print('Enviando "%s"' % message)

    sent = sock.sendto(message.encode("ascii"), multicast_group)

    while True:
        print('Esperando respuesta')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no se recibieron mas respuestas')
            break
        else:
            print('Recibido "%s" de %s' % (data, server))

finally:
    print('Socket cerrado')
    sock.close()
