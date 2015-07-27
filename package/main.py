import pysniffer as ps

 
class main(object):
    """main class for this module"""

    pl = ps.port_list(1,5000)
    pl.ListPortService()
    for port in pl.ValidPorts:
        print(port)

    strm = ps.packet_stream
    strm
    for packet in strm.header:
        __cnt = 0
        for element in packet:
            print(type(element))
            try:
                sourcePort = socket.inet_ntoa(element[__cnt])
                destinationPort = socket.inet_ntoa(element[__cnt+1])
                print('Source Port: ' + sourcePort)
                print('Destination Port: ' + destinationPort)
                __cnt = __cnt + 1
            except:
                print('Unexpected error:', sys.exc_info()[0])