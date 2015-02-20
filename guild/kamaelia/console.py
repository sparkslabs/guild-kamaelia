#!/usr/bin/python
"""
Less than ideal, but matches Kamaelia's implementation - which is ancient,
and was a bad idea. But hey, that's life.
"""

from guild.actor import *
import logging
import sys as _sys


#FIXME: This isn't ideal, but better than nothing for the moment
for actor_class_name in ["ConsoleEchoer" ]:
    logger = logging.getLogger(__name__ +"." + actor_class_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)



class ConsoleEchoer(Actor):
    def __init__(self, forwarder=False, use_repr=False, tag=""):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ConsoleEchoer, self).__init__()
        self.forwarder=forwarder
        if use_repr:
            self.serialise = repr
        else:
            self.serialise = str
        self.tag = tag

    @actor_method
    def input(self,data):
        _sys.stdout.write(self.tag + self.serialise(data))
        _sys.stdout.flush()
        if self.forwarder:
            self.output(data)

    @actor_method
    def control(self,data):
        self.signal(data)
        self.stop()

    @late_bind_safe
    def output(self, value):
        pass

    @late_bind_safe
    def signal(self, value):
        pass

    # For Kamaelia compatibility...
    inbox = input
    outbox = output


if __name__ == "__main__":
    import time
    from file import ReadFileAdaptor
    
    producer = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30)
    consumer = ConsoleEchoer()
    
    pipe(producer, "output", consumer, "input")
    pipe(producer, "signal", consumer, "control")
    
    start(producer, consumer)
    #time.sleep(6)

    #stop(producer, consumer)
    wait_for(producer, consumer)
