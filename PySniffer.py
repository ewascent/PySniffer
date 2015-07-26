#!/usr/bin/env python
import binascii
import io, os, platform, sys
import socket
import struct

# create a raw socket and bind it to the public interface. this is OS specific
# Third argument is often ignored/noop. IPPROTO_IP is for raw IP packets. IPPROTO_TCP and IPPROTO_UDP are higher level protocols.
# If you open an raw IP socket, you're responsible for assembling all the IP bytes yourself. 
# optionally use socket.htons(x) where x could be 0x0800. converts 16-bit positive integers from host to network byte order. 

if platform.system() == 'Linux':
    socketToMe=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.IPPROTO_IP)
elif platform.system() == 'Windows':
    socketToMe=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
else:
    socketToMe=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)

print(socket.getfqdn())
Hostess = socket.gethostbyname(socket.getfqdn())
print(Hostess)
# thou art bound to me, my love
socketToMe.bind((Hostess, 0))
socketToMe
#ifconfig eth0 promisc up

# receive all packages
allPackets = socketToMe.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
type(allPackets)
print('Show all packets: ' + str(allPackets))
# receive a package
receivedPacket=socketToMe.recv(2048)

#Ethernet Header...
ethernetHeader=receivedPacket[0:14]
ethrheader=struct.unpack('!6s6s2s',ethernetHeader)
destinationIP= binascii.hexlify(ethrheader[0])
sourceIP= binascii.hexlify(ethrheader[1])
protocol= binascii.hexlify(ethrheader[2])
#print('Destination: ' + destinationIP)
#print('Source: ' + sourceIP)
#print('Protocol: '+ protocol)

#IP Header... 
ipHeader=receivedPacket[14:34]
ipHdr=struct.unpack('!12s4s4s',ipHeader)
destinationIP=socket.inet_ntoa(ipHdr[2])
sourceIP=socket.inet_ntoa(ipHdr[1])
print('Source IP: ' + sourceIP)
print('Destination IP: ' + destinationIP)

#TCP Header...
tcpHeader=receivedPacket[34:54]
try:
    print('struct size for tcpHeader: ' + str(struct.calcsize(tcpHeader)))
except:
    print('Unexpected error:', sys.exc_info()[0])


class PacketStream(object):
    def __iter__(self):
        # we are dealing with C types here. refer to https://docs.python.org/2/library/struct.html#format-characters
        # and https://docs.python.org/2/library/struct.html#struct-alignment
        # store the length of the header for use in unpacking the struct
        cLenTCPH = str(len(tcpHeader))
        # format !:network, 2: length s: char(c) or str(python), struct to unpack
        for tcpHdr in struct.unpack('!'+ cLenTCPH + 's',tcpHeader):
            yield tcpHdr

class PortList(object):
    def __init__(self, startPort, endPort):
        self.startPort = startPort
        self.endPort = endPort

    def ListPortSerice(self):
        self.portRange = range(self.startPort, self.endPort)
        self.ValidPorts = []
        self.InvalidPorts = []

        for port in self.portRange:
            try:
                porter = socket.getservbyport(port)
                self.ValidPorts.append(['Port ' + str(port) + ' is used for ' + porter])
            except:
                self.InvalidPorts.append(['Port ' + str(port) + ' threw an exception and may not be in use:', sys.exc_info()[0]])

    def __iter__(self):
        return self.ValidPorts
        

portList = PortList(1,5000)
portList.ListPortSerice()
for port in portList.ValidPorts:
   print(port)

#instantiate PacketStream
stream = PacketStream()

for packet in stream:
    cnt = 0
    for element in packet:
        print(type(element))
        try:
            sourcePort = socket.inet_ntoa(element[cnt])
            destinationPort = socket.inet_ntoa(element[cnt+1])
            print('Source Port: ' + sourcePort)
            print('Destination Port: ' + destinationPort)
            cnt = cnt + 1
        except:
            print('Unexpected error:', sys.exc_info()[0])
