#!/usr/bin/python

"""
Less than ideal, but matches Kamaelia's implementation - which is ancient,
and was a bad idea. But hey, that's life.
"""
from guild.actor import *
import logging

#FIXME: This isn't ideal, but better than nothing for the moment
for actor_class_name in ["PureTransformer" ]:
    logger = logging.getLogger(__name__ +"." + actor_class_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class PureTransformer(Actor):
    def __init__(self, function=None):
        super(PureTransformer, self).__init__()
        self.function = function

    @actor_method
    def input(self,data):
        f = self.function 
        self.output(f(data))

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

if __name__ == "__main__":
    from chassis import Pipeline
    from console import ConsoleEchoer
    from readfileadaptor import ReadFileAdaptor

    Pipeline(
        Pipeline(ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=60)),
        PureTransformer(lambda x : "PRE:" + repr(x) + "\n"),
        ConsoleEchoer()
    ).run()
