import socket as sock
import select
from typing import Optional

class Peer:
    def __init__(self):
        pass

    # Gets the latest worldspace transform of the peer
    def Transform(self):
        return None

class Client:
    def __init__(self, port=None):
        self.sckt = sock.socket(
            family=sock.AF_INET,
            type=sock.SOCK_DGRAM,
            proto=sock.IPPROTO_UDP)
        self.sckt.setblocking(False)
        if port is None:
            port = 0 # Automatic
        self.sckt.bind(port)
        self.peers = []

    def SearchForPeers(self):
        self.sckt.listen()

    def GetPeer(self) -> Optional[Peer]:
        # see if we received a broadcast
        maxWait = 0.1
        readable, writeable, exceptional = select.select([self.sckt], [], [], maxWait)
        for r in readable:
            # do something
            packet = self.sckt.recv()
            id, transform = ExtractPacket(packet)
            
        # make a client if so