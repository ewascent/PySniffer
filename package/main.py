import pysniffer as snif
port_list = snif.port_list(1,5000)
stream = snif.packet_stream()
 
class main(object):
    """description of class"""
    def __init__(self):
        return self
        #instantiate port_list
        port_list.ListPortSerice()
        
        for port in port_list.ValidPorts():
            print(port)
    

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
main()
