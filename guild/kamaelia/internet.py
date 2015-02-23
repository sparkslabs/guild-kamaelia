#!/usr/bin/python
"""
Less than ideal, but matches Kamaelia's implementation - which is ancient,
and was a bad idea. But hey, that's life.
"""
from guild.actor import *
import logging
import sys as _sys
import time
import socket

#FIXME: This isn't ideal, but better than nothing for the moment
for actor_class_name in ["ServerCore", "FastRestartServer"]:
    logger = logging.getLogger(__name__ +"." + actor_class_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# class ServerCore(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):

class ServerCore(Actor):

    port = 1601
    protocol = None
    socketOptions=None
    # TCPS=TCPServer  
    def __init__(self, **argd):
        self.__dict__.update(argd)

        self.connectedSockets = []
        self.server = None
        if not self.protocol:
            print (self.__class__, self.__class__.protocol, self.protocol)
            raise TypeError("Need a protocol to handle!")

        super(ServerCore, self).__init__() 


class FastRestartServer(ServerCore):
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
