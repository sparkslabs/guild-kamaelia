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
    from guild.kamaelia import Graphline            # from Kamaelia.Chassis.Graphline
    from guild.kamaelia import PAR                  # from Kamaelia.Chassis.PAR
    from guild.kamaelia import PureTransformer      # from Kamaelia.Util.PureTransformer

## WIP

    from guild.kamaelia import Backplane            # from Kamaelia.Util.Backplane
    from guild.kamaelia import PublishTo            # from Kamaelia.Util.Backplane
    from guild.kamaelia import SubscribeTo          # from Kamaelia.Util.Backplane

## Core

These aren't written yet.

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

## Undecided / Unplanned

The following list of components was generated as follows ...

    find -type f |grep py$ | while read filename; do
         grep __kamaelia_components__ $filename |
         sed -e "s/__kamaelia_components__  *=  *//g" ; 
     done | egrep '^\([^)]'|sed -e "s/^(//g; s/) *$//g"|while read c; do
         echo -n $c;
     done|sed -e "s/,/ /g"|sed -e "s/  */\n/g"|sort|uniq

... and then tidied up, with the components above removed.

In particular these aren't planned to be worked, and I'm currently undecided
as to whether they should even be worked on.

    AIMHarness
    Annotator
    Append
    ArrowButton
    AudioCookieProtocol
    bouncingFloat
    Button
    ByteRate_RequestControl
    CallbackStyleComponent
    cartesianPingPong
    Chargen
    ChatManager
    CheapAndCheerfulClock
    Chooser
    ChunkNamer
    chunks_to_lines
    CollabParser
    CollabWithViewParser
    Collate
    Comparator
    ConcreteMailHandler
    Container
    continuousIdentity
    continuousOne
    continuousZero
    TorrentMaker
    DataSource
    Decoder
    DeFramer
    DeMarshaller
    DemuxerService
    DetectShotChanges
    DictChooser
    DiracDecoder
    DiracEncoder
    AOAudioPlaybackAdaptor
    Duplicate
    DVB_Demuxer
    DVB_Multiplex
    DVB_SoftDemuxer
    EchoProtocol
    echo
    EITPacketParser
    Encoder
    ERModel2Visualiser
    ERParser
    Fanout
    FastRestartSingleServer
    Filter
    FilterOutNotCurrent
    FirstOnly
    FortuneCookieProtocol
    ForwardIteratingChooser
    Framer
    FrameToYUV4MPEG
    GraphSlideXMLComponent
    GreyListingPolicy
    HelloServer
    HTTPMakePostRequest
    HTTPParser
    HTTPShutdownLogicHandling
    HTTPRequestHandler
    IcecastClient
    IcecastDemux
    IcecastStreamWriter
    SimpleHTTPClient
    Image
    ImageButton
    Input
    IntelligentFileReader
    Interactor
    Introspector
    JSONDecoderNowNextServiceFilter
    JSONEncoder
    KeyEvent
    Label
    LiftTranslationInteractor
    LineSplit
    lines_to_tokenlists
    LoginHandler
    loopingCounter
    LossyConnector
    LPF
    MagnaDoodle
    MailHandler
    Marshaller
    MatchedTranslationInteractor
    Max
    MaxSpeedFileReader
    MimeRequestComponent
    Minimal
    Multicast_receiver
    Multicast_sender
    Multicast_transceiver
    Multiclick
    NowNextChanges
    NowNextServiceFilter
    NullPayloadPreFramer
    OnDemandLimit
    OneShot
    OpenGLComponent
    OpenGLDisplay
    OSCARProtocol
    Output
    Paint
    ParseEventInformationTable
    ParseNetworkInformationTable
    ParseProgramAssociationTable
    ParseProgramMapTable
    ParseServiceDescriptionTable
    ParseTimeAndDateTable
    ParseTimeOffsetTable
    PassThrough
    PathMover
    PeriodicWakeup
    Plug
    PlugSplitter
    PostboxPeer
    PrettifyProgramAssociationTable
    ProgressBar
    PromptedTurnstile
    PSIPacketReconstructor
    PyGameApp
    PygameDisplay
    PygameWrapper
    RangeFilter
    RateChunker
    RawAudioMixer
    RawYUVFramer
    RDFParser
    ReassemblePSITables
    RecoverOrder
    ReorderSimplePeer
    Resample
    RTPDeframer
    RTPFramer
    RtpPacker
    SDPParser
    Selector
    SequentialTransformer
    SessionExample
    SimpleButton
    SimpleBuzzer
    SimpleCube
    SimpleFileWriterWithOutput
    SimpleMover
    SimplePeer
    SimpleReaderChunkifier
    SimpleRotationInteractor
    SimpleRotator
    SimpleTranslationInteractor
    SimpleXMLParser
    SingleServer
    SingleShotHTTPClient
    SkyGrassBackground
    SNACExchanger
    SpeexDecode
    SpeexEncode
    Splitter
    StandardStyleComponentMaxSizePacketiser
    Stringify
    Subscribe
    Sync
    TagWithSequenceNumber
    TargettedPeer
    TestResult
    TexPlane
    Textbox
    TextDisplayer
    ThreadedTCPClient
    Throwaway
    Ticker
    TimeAndDatePacketParser
    tkInvisibleWindow
    TkWindow
    TopologyViewer
    TopologyViewer3D
    TopologyViewer3DWithParams
    ToRGB_interleaved
    TorrentClient
    TorrentPatron
    TorrentService
    ToService
    ToYUV420_planarCropAndScale
    TriggeredFileReader
    TriggeredOneShot
    Tuner
    UDPReceiver
    UDPSender
    UnixProcess2
    UnseenOnly
    UploadTorrents
    VariableByteRate_RequestControl
    VideoOverlay
    VideoSurface
    VorbisDecode
    WakeableIntrospector
    WAVParser
    WAVWriter
    WheelMover
    WholeFileWriter
    YUV4MPEGToFrame
