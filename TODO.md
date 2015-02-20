## The Todo list

This is a list of components that need writing, where they will sit
in the namespace and where they sit inside the Kamaelia namespace.
They'll probably actually exist inside specific files and be pulled in,
but the API will remain this. Probably.

Key point - this isn't about improving or changing the component functionality, but 
about bringing the functionality into Guild with the same API as Kamaelia - for good
or ill. This is why this is a seperate project from guild.

## NOTE

**The chassis components here are hideously inefficient, and are NOT the preferred**
**way of running a guild system. They are provided for compatibility only.**

It might be they improve though.

## Done

    from guild.kamaelia import ReadFileAdaptor      # from Kamaelia.File.ReadFileAdaptor
    from guild.kamaelia import ConsoleEchoer        # from Kamaelia.Util.Console
    from guild.kamaelia import Pipeline             # from Kamaelia.Chassis.Pipeline

## WIP

    from guild.kamaelia import Graphline            # from Kamaelia.Chassis.Graphline

## Core

These aren't written yet.

    from guild.kamaelia import PureTransformer      # from Kamaelia.Util.PureTransformer
    from guild.kamaelia import PAR                  # from Kamaelia.Chassis.PAR
    from guild.kamaelia import Backplane            # from Kamaelia.Util.Backplane
    from guild.kamaelia import PublishTo            # from Kamaelia.Util.Backplane
    from guild.kamaelia import SubscribeTo          # from Kamaelia.Util.Backplane
    from guild.kamaelia import SimpleFileWriter     # from Kamaelia.File.Writing
    from guild.kamaelia import FastRestartServer    # from Kamaelia.Chassis.ConnectedServer
    from guild.kamaelia import TCPClient            # from Kamaelia.Internet.TCPClient
    from guild.kamaelia import ConsoleReader        # from Kamaelia.Util.Console 
    from guild.kamaelia import UnixProcess          # from Kamaelia.File.UnixProcess
    from guild.kamaelia import DataDeChunker        # from Kamaelia.Protocol.Framing
    from guild.kamaelia import DataChunker          # from Kamaelia.Protocol.Framing
    from guild.kamaelia import Carousel             # from Kamaelia.Chassis.Carousel

Items marked # should be done first

## Required by Core:

These aren't written yet.

    from guild.kamaelia import SimpleServer         # from Kamaelia.Chassis.ConnectedServer
    from guild.kamaelia import ServerCore           # from Kamaelia.Chassis.ConnectedServer
    from guild.kamaelia import NoActivityTimeout    # from Kamaelia.Internet.TimeOutCSA
    from guild.kamaelia import TCPServer            # from Kamaelia.Internet.TCPServer
    from guild.kamaelia import ConnectedSocketAdapter   # from Kamaelia.Internet.ConnectedSocketAdapter

## Secondary:

These aren't written yet.

    from guild.kamaelia import Seq                  # from Kamaelia.Chassis.Seq import Seq
    from guild.kamaelia import TwoWaySplitter       # from Kamaelia.Util.TwoWaySplitter
    from guild.kamaelia import MessageRateLimit     # from Kamaelia.Util.RateFilter
    from guild.kamaelia import nullSinkComponent    # from Kamaelia.Util.NullSink
    from guild.kamaelia import SimpleDetupler       # from Kamaelia.Util.Detuple
    from guild.kamaelia import PromptedFileReader   # from Kamaelia.File.Reading
    from guild.kamaelia import RateControlledFileReader # from Kamaelia.File.Reading

## Ideas arising

### Possible new names or alternatives for Graphline

In particular, worth noting that Graphline actually subsumbes the
functionality of PAR

from guild.kamaelia import Breadboard # Graphline?  No, no new names in this namespace
from guild.kamaelia import Composite # Graphline?   No, no new names in this namespace
from guild.kamaelia import Compound # Graphline?   No, no new names in this namespace

