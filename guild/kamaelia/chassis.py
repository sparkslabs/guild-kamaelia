#!/usr/bin/python
"""
Less than ideal, but matches Kamaelia's implementation - which is ancient,
and was a bad idea. But hey, that's life.
"""
from guild.actor import *
import logging
import sys as _sys


#FIXME: This isn't ideal, but better than nothing for the moment
for actor_class_name in ["Pipeline", "Graphline" ]:
    logger = logging.getLogger(__name__ +"." + actor_class_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class Graphline(Actor):
    # First of all we'll aim for graphlines with just standard inboxes/outboxes...
    def __init__(self, linkages = None, **components):
        self.layout = linkages
        self.components = dict(components)

        self.border_inlinks = {}
        self.border_outlinks = {}

        super(Graphline,self).__init__()

        if self.layout:
            for componentRef,sourceBox in self.layout:
                toRef, toBox = self.layout[(componentRef,sourceBox)]

                fromComponent = self.components.get(componentRef, self)
                toComponent = self.components.get(toRef, self)
                if fromComponent == self or toComponent == self:
                    self.borderLinkage(fromComponent, sourceBox, toComponent, toBox)
                    continue # Don't make a linkage!

                pipe(fromComponent, sourceBox, toComponent, toBox)

    def borderLinkage(self, fromComponent, sourceBox, toComponent, toBox):
        if fromComponent == self:
            self.border_inlinks[sourceBox] = toComponent, toBox
            setattr(self, sourceBox, getattr(toComponent, toBox))

        else:
            self.border_outlinks[toBox] = fromComponent, sourceBox

    @actor_method
    def bind(self, source_box, dest, destmeth):
        # Bind our output function to their input
        # In this case it means bind our last child's output...
        if len(self.components.values()):
            component, methodname = self.border_outlinks[source_box]
            component.bind(methodname, dest, destmeth)

    def process_start(self):

        for c in self.components.values():
            c.go()

    @process_method
    def process(self):
        "Check to see if the child processes are running. If they aren't, stop"
        if len(self.components.values()) >0:
            time.sleep(0.001) # Only rarely check.
            children_running = False
            for component in self.components.values():
                children_running = children_running or component.is_alive()
            if not children_running:
                for component in self.components.values():
                    component.join()
                self.stop()

    # These should be bypassed, except in the empty state
    @actor_method
    def input(self, data):
        try:
            toComponent, toBox = self.border_inlinks["input"]
            func = getattr(toComponent, toBox)
            func(data)
        except:
            pass

    @actor_method
    def control(self, data):
        try:
            toComponent, toBox = self.border_inlinks["control"]
            func = getattr(toComponent, toBox)
            func(data)
        except:
            pass

class Pipeline(Actor):
    circular = False
    def __init__(self, *components, **argv):
        super(Pipeline,self).__init__()
        self.components = list(components)
        try:
            self.input = self.components[0].input
        except:
            pass
        try:
            self.control = self.components[0].control
        except:
            pass
        
    def process_start(self):
        if len(self.components) > 0:
            last = self.components[0]
            for dest in self.components[1:]:
                pipe(last,"output", dest,"input") # FIXME: Should this be inbox/input , outbox/output ?
                pipe(last,"signal", dest,"control")
                last = dest # Keep track of last
            if self.circular:
                pipe(last,"output", self.components[0],"input") # FIXME: Should this be inbox/input , outbox/output ?
                pipe(last,"signal", self.components[0],"control")

            for dest in self.components:
                dest.go()

    @process_method
    def process(self):
        "Check to see if the child processes are running. If they aren't, stop"
        if len(self.components) >0:
            time.sleep(0.001) # Only rarely check.
            children_running = False
            for component in self.components:
                children_running = children_running or component.is_alive()
            if not children_running:
                for component in self.components:
                    component.join()
                self.stop()

    @actor_method
    def bind(self, source_box, dest, destmeth):
        # Bind our output function to their input
        # In this case it means bind our last child's output...
        if len(self.components):
            self.components[-1].bind(source_box, dest, destmeth)
        else:
            super(Pipeline, self).bind(source_box, dest, destmeth)

    # These are bypassed, except in the empty state
    @actor_method
    def input(self, data):
        try:
            self.components[0].input(data)
        except IndexError:
            self.output(data)
 
    @actor_method
    def control(self, data):
        try:
            self.components[0].control(data)
        except IndexError:
            self.signal(data)
            self.stop() # FIXME: Assume some kind of shutdown message along signal


    # These two are for introspection, but will not actually be bound to.
    @late_bind_safe
    def output(self, value):
        pass

    @late_bind_safe
    def signal(self, value):
        pass

if __name__ == "__main__":
    import time
    from readfileadaptor import ReadFileAdaptor
    from console import ConsoleEchoer
    g = Graphline(
                    source = Graphline(
                                RFA = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                linkages = {
                                    ("RFA", "output") : ("self", "d_output"),
                                    ("RFA", "signal") : ("self", "d_signal")
                                    }
                            ),
                    sink = Graphline(
                                ce = ConsoleEchoer(tag="** BASICTEST 1**"),
                                linkages = {
                                    ("self", "d_input") : ("ce", "input"),
                                    ("self", "d_control") : ("ce", "control")
                                    }
                            ),
                    linkages = {
                        ("source","d_output") : ("sink","d_input"),
                        ("source","d_signal") : ("sink","d_control")
                    }

                )

    g.go()
    wait_for(g)


    if 0:
        g = Graphline(
                        source = Graphline(
                                    RFA = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    linkages = {
                                        ("RFA", "output") : ("self", "d_output"),
                                        ("RFA", "signal") : ("self", "d_signal")
                                        }
                                ),
                        sink = Graphline(
                                    ce = ConsoleEchoer(tag="** BASICTEST 1**"),
                                    linkages = {
                                        ("self", "input") : ("ce", "input"),
                                        ("self", "control") : ("ce", "control")
                                        }
                                ),
                        linkages = {
                            ("source","d_output") : ("sink","input"),
                            ("source","d_signal") : ("sink","control")
                        }

                    )

        g.go()
        wait_for(g)

        g = Graphline(
                        source = Graphline(
                                    RFA = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    linkages = {
                                        ("RFA", "output") : ("self", "output"),
                                        ("RFA", "signal") : ("self", "signal")
                                        }
                                ),
                        sink = Graphline(
                                    ce = ConsoleEchoer(tag="** BASICTEST 1**"),
                                    linkages = {
                                        ("self", "input") : ("ce", "input"),
                                        ("self", "control") : ("ce", "control")
                                        }
                                ),
                        linkages = {
                            ("source","output") : ("sink","input"),
                            ("source","signal") : ("sink","control")
                        }

                    )

        g.go()
        wait_for(g)
        p = Pipeline(
                        Graphline(
                                    RFA = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    linkages = {
                                        ("RFA", "output") : ("self", "output"),
                                        ("RFA", "signal") : ("self", "signal")
                                        }
                                ),
                        Graphline(
                                    ce = ConsoleEchoer(tag="** BASICTEST 1**"),
                                    linkages = {
                                        ("self", "input") : ("ce", "input"),
                                        ("self", "control") : ("ce", "control")
                                        }
                                )
                    )

        p.go()
        wait_for(p)
        p = Pipeline(
                        Graphline(
                                    RFA = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    linkages = {
                                        ("RFA", "output") : ("self", "output"),
                                        ("RFA", "signal") : ("self", "signal")
                                        }
                                ),
                        ConsoleEchoer(tag="** BASICTEST 1**"),
                    )

        p.go()
        wait_for(p)

        p = Pipeline(
                    ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                    Graphline(
                                ce = ConsoleEchoer(tag="** BASICTEST 1**"),
                                linkages = {
                                    ("self", "input") : ("ce", "input"),
                                    ("self", "control") : ("ce", "control")
                                    }
                            )
                    )

        p.go()
        wait_for(p)


        g = Graphline(
                    p1 = Pipeline(
                                    ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    ConsoleEchoer(tag="** BASICTEST 1**")
                                ),
                    p2 = Pipeline(
                                    ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    ConsoleEchoer(tag="** BASICTEST 1**")
                                )
            )
        g.go()
        wait_for(g)

        # This usecase is very similar to PAR
        #
        g = Graphline(
                    p = Pipeline(
                                    ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                                    ConsoleEchoer(tag="** BASICTEST 1**")
                                )
            )
        g.go()
        wait_for(g)
        g = Graphline(
                source = ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                sink = ConsoleEchoer(tag="** BASICTEST 1**"),
                linkages = {
                    ("source","output") : ("sink","input"),
                    ("source","signal") : ("sink","control")
                }
            )
        g.go()
        wait_for(g)

    if 0:
        p = Pipeline(
                    ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                    ConsoleEchoer(tag="** BASICTEST 1**")
            )
        p.go()
        wait_for(p)

        p = Pipeline(
                    ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30),
                    Pipeline(),
                    ConsoleEchoer(tag="** BASICTEST 2**")
            )
        p.go()
        wait_for(p)

        p = Pipeline(
                    Pipeline(ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30)),
                    ConsoleEchoer(tag="** BASICTEST 3**")
            )
        p.go()
        wait_for(p)

        p = Pipeline(
                    Pipeline(ReadFileAdaptor("console.py", readmode="bitrate", chunkrate=30)),
                    ConsoleEchoer(tag="** BASICTEST 4**")
            )
        p.go()
        wait_for(p)
