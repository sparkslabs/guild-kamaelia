#!/usr/bin/python

"""
Less than ideal, but matches Kamaelia's implementation - which is ancient,
and was a bad idea. But hey, that's life.
"""
from guild.actor import *
from guild.components import Backplane as _gBackplane
from guild.components import PublishTo as _gPublishTo
from guild.components import SubscribeTo as _gSubscribeTo
import logging

import time

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

class Backplane(Actor):
    def __init__(self, name):
        super(Backplane,self).__init__()
        self.name = "__kam_" + name
        self.bp = _gBackplane(self.name)

    def process_start(self):
        self.bp.go()

    @process_method
    def process(self):
        time.sleep(0.5)
        if not(self.bp.is_alive()):
            self.stop()
            return False

    @actor_method
    def control(self,data):
        self.signal(data)
        self.stop()

    @late_bind_safe
    def signal(self, value):
        pass

class PublishTo(Actor):
    # FIXME: Does not implement the forwarding interface
    # Would be nice if this forwarded control AND data signals
    def __init__(self, name):
        super(PublishTo, self).__init__()
        self.name = "__kam_" + name
        self.bp = _gPublishTo(self.name)

    @actor_method
    def input(self, data):
        self.bp.publish(data)
    
    @actor_method
    def control(self, data):
        self.signal(data)
        self.stop()

    @late_bind_safe
    def signal(self, value):
        pass

class SubscribeTo(Actor):
    # Would be nice if this unpacked control AND data signals
    def __init__(self, name):
        super(SubscribeTo, self).__init__()
        self.name = "__kam_" + name
        self.sub = _gSubscribeTo(self.name)

    def process_start(self):
        self.sub.go()

    @actor_method
    def input(self, data):
        pass

    @actor_method
    def control(self, data):
        self.signal(data)
        self.sub.stop()
        self.sub.join()
        self.stop()

    @actor_method
    def bind(self, source_box, dest, destmeth):
        # Bind our output function to their input
        # In this case it means bind our last child's output...
        if source_box == "output":
            self.sub.bind("output", dest, destmeth)
        else:
            super(SubscribeTo, self).bind(source_box, dest, destmeth)

    @late_bind_safe
    def signal(self, value):
        pass

if __name__ == "__main__":
    from chassis import Pipeline
    from console import ConsoleEchoer
    from readfileadaptor import ReadFileAdaptor

    bp = Backplane("Example").go()

    p1 = Pipeline(
                    Pipeline(ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=60)),
                    PublishTo("Example")
                 ).go()

    p2 = Pipeline(
                    SubscribeTo("Example"),
                    ConsoleEchoer()
                 ).go()

    wait_KeyboardInterrupt()


    if 0:
        Pipeline(
            Pipeline(ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=60)),
            PureTransformer(lambda x : "PRE:" + repr(x) + "\n"),
            ConsoleEchoer()
        ).run()
