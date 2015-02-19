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


class Pipeline(component):
    circular = False
    def __init__(self, *components, **argv):
        (Pipeline,self).__init__(**argv)
        self.components = list(components)
        self.input = self.components[0].input
        self.control = self.components[0].control
        
    def process_start(self):
        last = self.components[0]
        for dest in self.components[1:]:
            pipe(last,"output", dest,"input") # FIXME: Should this be inbox/input , outbox/output ?
            pipe(last,"signal", dest,"control")
            last = dest # Keep track of last
      if self.circular:
            pipe(last,"output", self.components[0],"input") # FIXME: Should this be inbox/input , outbox/output ?
            pipe(last,"signal", self.components[0],"control")

    @process_method
    def process(self):
        "Check to see if the child processes are running. If they aren't, stop"
        time.sleep(0.5) # Only rarely check.
        children_running = True
        for component in self.components:
            children_running = children_running or component.is_alive()
        if not children_running:
            self.stop()

    @actor_method
    def bind(self, source_box, dest, destmeth):
        # Bind our output function to their input
        # In this case it means bind our last child's output...
        self.components[-1].bind(source_box, dest, destmeth)

    # These are probably bypassed, but for now left in place.
    @actor_method
    def input(self, data):
       self.components[0].input(data)
 
    @actor_method
    def control(self, data):
       self.components[0].control(data)


    # These two are for introspection, but will not actually be bound to.
    @late_bind_safe
    def output(self, value):
        pass

    @late_bind_safe
    def signal(self, value):
        pass
