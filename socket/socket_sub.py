#! /usr/bin/python
# ==============================================================================
# Copyright © 2019 Lavle USA Inc.
#
# This file is the property of Lavle USA Inc. and shall not be reproduced,
# copied, or used as the basis for the manufacture or sale of equipment without
# the express written permission of Lavle USA Inc.
# ==============================================================================
# Description:
#   This prototype demonstrates publishing information and receiving information 
#   over sockets. If the script does not work, change the IP address to your 
#   server.
# ==============================================================================
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 10222))
sock.setsockopt(socket.IPPROTO_IP,
                socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton("239.0.0.1") +
                socket.inet_aton("192.168.1.111"))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(1024)

    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data

    print >>sys.stderr, 'sending acknowledgement to', address
    sock.sendto('ack', address)
