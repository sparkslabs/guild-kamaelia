#!/usr/bin/python

"""
Less than ideal, but matches Kamaelia's implementation - which is ancient,
and was a bad idea. But hey, that's life.
"""
from guild.actor import *
import time
import os
import logging
import math

#FIXME: This isn't ideal, but better than nothing for the moment
for actor_class_name in ["ReadFileAdaptor", "SimpleFileWriter" ]:
    logger = logging.getLogger(__name__ +"." + actor_class_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

#FIXME: Probably ought to shift out from here.
class producerFinished(object):
   def __init__(self,caller=None,message=None):
      self.caller = caller
      self.message = message

class ReadFileAdaptor(Actor):
    def __init__(self, filename="",
                       command="",
                       readmode="",
                       readsize=1450,
                       steptime=0.0,
                       bitrate = 65536.0,        # Overrides readsize
                       chunkrate = 24,           # Overrides steptime
                       debug=0):
        super(ReadFileAdaptor, self).__init__()
        self.filename = filename
        self.command = command
        self.readmode = readmode
        self.bitrate = bitrate
        self.chunkrate = chunkrate
        self.debug = debug
        self.readsize = readsize
        self.steptime = steptime
        self.getData = self.getDataByteLen
        self.time = time.time()
        self.tosend = []

        if readmode=="bitrate":
            self.bitrate = bitrate
            self.chunkrate = chunkrate
            self.steptime = 1.0 / chunkrate        # Internally bitrate is semantic sugar for block mode.
            self.readsize = int(math.ceil((bitrate/8) / chunkrate))
            self.getData = self.getDataByteLen

        if readmode=="line" or not(readmode):
            self.getData = self.getDataReadline
            self.steptime = steptime

    def process_start(self):
        """Opens the appropriate file handle"""
        if self.filename:
            self.f = open(self.filename, "rb",0)
        else:
            if self.command:
                self.f = os.popen(self.command)
            else:
                self.f = sys.stdin

    def closeDownComponent(self):
        """Closes the file handle"""
        self.f.close()

    def getDataByteLen(self):
        """This method attempts to read data of a specific block size from
        the file handle. If null, the file is EOF. This method is never called
        directly. If the readmode is block or bitrate, then the attribute self.getData
        is set to this function, and then this function is called using self.getData().
        The reason for this indirection is to make it so that the check for
        which readmode we are in is done once, and once only"""
        data = ""
        data = self.f.read(self.readsize)
        if not data:
            self.signal( producerFinished(self) )
            self.stop()
        return data

    def getDataReadline(self):
        """This method attempts to read a line of data from the file handle.
        If null, the file is EOF. As with getDataByteLen, this method is never called
        directly. If the readmode is readline (or ""), then the attribute self.getData
        is set to this function, and then this function is called using self.getData().
        Same reason for indirection as above."""
        data = self.f.readline()
        if not data:
            self.signal( producerFinished(self) )
            self.stop()
        return data

    @process_method
    def process(self):
        """We check whether it's time to perform a new read, if it is, we
        read some data. If we get some data, we put it in out outbox
        "outbox", and to stdout (if debugging).
        If we had an error state (eg EOF), we return 0, stopping this component, otherwise
        we return 1 to live for another line/block.
        """
        if len(self.tosend)>0:
            for data in self.tosend:
                try:
                    self.output(data) # We kinda assume people are listening...
                except UnboundActorMethod:
                    time.sleep(0.01)
                    return
            self.tosend = []
            
        if ((time.time() - self.time) > self.steptime):
            self.time = time.time()
            data = self.getData()

            if data:
                try:
                    self.output(data) # We kinda assume people are listening...
                except UnboundActorMethod:
                    self.tosend.append(data)
                    return
                if self.debug:
                    sys.stdout.write(data)
                    sys.stdout.flush()
            else:
                return False # Exit the loop

    @actor_method
    def control(self,data):
        self.signal(data)
        self.stop()

    @late_bind_safe
    def signal(self, signal_data):
        pass

    @late_bind
    def output(self, data):
        pass

    # For Kamaelia compatibility...
    inbox = input
    outbox = output

class SimpleFileWriter(Actor):
    def __init__(self, filename, mode = "wb"):
        self.filename = filename
        self.mode = mode
        super(SimpleFileWriter, self).__init__()

    def process_start(self):
        self.fh = open(self.filename, self.mode, 0)

    @actor_method
    def input(self, data):
        self.fh.write(data)

    @late_bind_safe
    def output(self, data):
        pass

    @late_bind_safe
    def signal(self, signal_data):
        pass

    @actor_method
    def control(self,data):
        self.signal(data)
        self.stop()


if __name__ == "__main__":
    import sys
    class Printer(Actor):
        @actor_method
        def Print(self, *argv):
            _argv = list(argv)
            str_argv = [str(x) for x in _argv]
            argv_print = " ".join(str_argv)
            sys.stderr.write(argv_print)
            sys.stderr.write("\n")

    from chassis import Pipeline
    from util import PureTransformer
    
    testfile="file.py"
    p = Pipeline(
            ReadFileAdaptor(testfile, chunkrate=30),
            PureTransformer(lambda x : x.rstrip()),
            PureTransformer(lambda y : time.asctime() + ":" + y + "\n"),
            SimpleFileWriter("testfile")
        )

    p.go()
    wait_for(p)

    if 0:
        p = Printer().go()
        rfa = ReadFileAdaptor(testfile, readmode="bitrate", bitrate=420, chunkrate=30,debug=1).go()
        pipe(rfa, "output", p, "Print")
        
        wait_for(rfa)
        p.stop()
        wait_for(p)



