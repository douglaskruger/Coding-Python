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
#   over sockets.
# ==============================================================================
import socket

MCAST_GRP = '224.0.0.1'
MCAST_GRP = '239.0.0.1'
MCAST_PORT = 10222

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton("192.168.1.111"))
sock.sendto("HELLO!!!!! Using Group: 239.0.0.1 Port: 10222", (MCAST_GRP, MCAST_PORT))
