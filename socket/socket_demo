#!/bin/sh
# ==============================================================================
# Copyright © 2019 Lavle USA Inc.
#
# This file is the property of Lavle USA Inc. and shall not be reproduced,
# copied, or used as the basis for the manufacture or sale of equipment without
# the express written permission of Lavle USA Inc.
# ==============================================================================
# Description:
#   This prototype demonstrates publishing information and receiving information 
#   over sockets. It is the master driver script. If the script does not work, 
#   check the IP addresses in the scripts. Beware that the python runs in the 
#   background - so it may live beyond exiting this demo script - so you may 
#   need to kill it separately.
# ==============================================================================
#
# Sample output
# waiting to receive message
# received 45 bytes from ('192.168.1.111', 47768)
# HELLO!!!!! Using Group: 239.0.0.1 Port: 10222
# sending acknowledgement to ('192.168.1.111', 47768)
# 
# waiting to receive message
# received 45 bytes from ('192.168.1.111', 44289)
# HELLO!!!!! Using Group: 239.0.0.1 Port: 10222
# sending acknowledgement to ('192.168.1.111', 44289)

# Run the listener in the background
(socket_sub &)

while [ 1 ]; do
	# Publish a new record once per second
	socket_pub
	sleep 1
done
