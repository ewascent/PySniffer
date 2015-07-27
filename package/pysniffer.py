#!/usr/bin/env python
import binascii
import io, os, platform, sys
import socket
import struct

# create a raw socket and bind it to the public interface. this is OS specific
# Third argument is often ignored/noop. IPPROTO_IP is for raw IP packets. IPPROTO_TCP and IPPROTO_UDP are higher level protocols.
# If you open an raw IP socket, you're responsible for assembling all the IP bytes yourself. 
# optionally use socket.htons(x) where x could be 0x0800. converts 16-bit positive integers from host to network byte order. 

class socket_wrench(object):
    def __init__(self):
        os_platform = platform.system()
        return self

    def return_socket(self):
        if self.os_platform == 'Linux':
            socketToMe=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.IPPROTO_IP)
        elif self.os_platform == 'Windows':
            socketToMe=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
        else:
            socketToMe=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
        
        print(socket.getfqdn())
        self.hostess = socket.gethostbyname(socket.getfqdn())
        print(self.hostess)
        # thou art bound to me, my love
        socketToMe.bind((self.hostess, 0))
        #ifconfig eth0 promisc up
        
        # receive all packages
        self.all_packets = socketToMe.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        type(self.all_packets)
        print('Show all packets: ' + str(self.all_packets))
        # receive a package
        self.received_packet=socketToMe.recv(2048)

        return self.received_packet

class ethernet_header(object):
    def __init__(self):
        s = socket_wrench()
        socket_to_me = s.return_socket()
    def ethernet_details(self):
        ethernetHeader=socket_to_me.received_packet[0:14]
        ethrheader=struct.unpack('!6s6s2s',ethernetHeader)
        destinationIP= binascii.hexlify(ethrheader[0])
        sourceIP= binascii.hexlify(ethrheader[1])
        protocol= binascii.hexlify(ethrheader[2])
        print('Destination: ' + destinationIP)
        print('Source: ' + sourceIP)
        print('Protocol: '+ protocol)
        return self

class ip_header(object):
    def __init__(self):
        s = socket_wrench()
        socket_to_me = s.return_socket()
    def ip_details(self):
        self.ipHeader=socket_to_me.received_packet[14:34]
        self.ipHdr=struct.unpack('!12s4s4s',self.ipHeader)
        self.destinationIP=socket.inet_ntoa(self.ipHdr[2])
        self.sourceIP=socket.inet_ntoa(self.ipHdr[1])
        print('Source IP: ' + self.sourceIP)
        print('Destination IP: ' + self.destinationIP)

        return self

class tcp_header(object):
    def __init__(self):
        return self
    def tcp_details(self):
        s = socket_wrench()
        self.socket_to_me = s.return_socket()
        tcpHeader=socket_to_me.received_packet[34:54]
        try:
            print('struct size for tcpHeader: ' + str(struct.calcsize(tcpHeader)))
        except:
            print('Unexpected error:', sys.exc_info()[0])

        return self

class packet_stream(object):
    def __iter__(self):
        # we are dealing with C types here. refer to https://docs.python.org/2/library/struct.html#format-characters
        # and https://docs.python.org/2/library/struct.html#struct-alignment
        # store the length of the header for use in unpacking the struct
        h = tcp_header()
        headers = h.tcp_details()
        headerlen = str(len(headers))
        # format !:network, 2: length s: char(c) or str(python), struct to unpack
        for self.header in struct.unpack('!'+ headerlen + 's',headers):
            return self.header

        #return self.header

class port_list(object):
    def __init__(self, startPort, endPort):
        self.startPort = startPort
        self.endPort = endPort

    def ListPortService(self):
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
        