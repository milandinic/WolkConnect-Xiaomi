from past.builtins import basestring
import socket
import binascii
import struct
import json
from Crypto.Cipher import AES
import binascii
import time
import logging
from XiaomiConnect.Config import AutoConfig

logger = logging.getLogger(__name__)

class XiaomiConnector:
    """Connector for the Xiaomi Mi Hub and devices on multicast."""

    MULTICAST_PORT = 9898
    SERVER_PORT = 4321

    MULTICAST_ADDRESS = '224.0.0.50'
    SOCKET_BUFSIZE = 1024
    IV = bytes.fromhex('17996d093d28ddb3ba695a2e6f58562e')
    counter = 0
    initalDataLoaded = False

    def __init__(self, gatewayPassword, data_callback=None, config = None):
        """Initialize the connector."""
        self.data_callback = data_callback
        self.last_tokens = dict()
        self.socket = self._prepare_socket()
        self.gatewayPassword = gatewayPassword

        self.nodes = dict()
        self.config = config

    def _prepare_socket(self):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

        sock.bind(("0.0.0.0", self.MULTICAST_PORT))

        mreq = struct.pack("=4sl", socket.inet_aton(self.MULTICAST_ADDRESS), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.SOCKET_BUFSIZE)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        return sock

    def check_incoming(self):
        data, addr = self.socket.recvfrom(self.SOCKET_BUFSIZE)
        try:
            payload = json.loads(data.decode("utf-8"))
            logger.info("Received data")
            logger.debug(str(payload))
            self.handle_incoming_data(payload)          

        except Exception as e:
            raise
            logger.error("Can't handle message %r (%r)" % (data, e))

    def handle_incoming_data(self, payload):
        """Handle an incoming payload, save related data if needed,
        and use the callback if there is one.
        """
        if isinstance(payload.get('data', None), basestring):
            cmd = payload["cmd"]
            if cmd in ["heartbeat", "report", "read_ack"]:
                if self.data_callback is not None:
                    self.data_callback(payload["model"],
                                       payload["sid"],
                                       payload["cmd"],
                                       json.loads(payload["data"]))

            if cmd == "read_ack" and payload["sid"] not in self.nodes:
                self.nodes[payload["sid"]] = dict(model=payload["model"])

            if cmd == "heartbeat" and payload["sid"] not in self.nodes:
                self.nodes[payload["sid"]] = json.loads(payload["data"])
                self.nodes[payload["sid"]]["model"] = payload["model"]
                self.nodes[payload["sid"]]["sensors"] = []

            if cmd == "get_id_list_ack":
                device_sids = json.loads(payload["data"])
                self.nodes[payload["sid"]]["nodes"] = device_sids

                for sid in device_sids:
                    self.request_current_status(sid)

        if "token" in payload:
            self.last_tokens[payload["sid"]] = payload['token']
            if self.nodes[payload["sid"]]["model"] == "gateway" and self.config.gatewayId != None and self.initalDataLoaded == False:
                self.initalDataLoaded = True
                self.request_sids(self.config.gatewayId)

    def request_sids(self, sid):
        """Request System Ids from the hub."""
        logger.info("request_sids " + str(sid))
        self.send_command({"cmd": "get_id_list", sid: sid})

    def request_current_status(self, device_sid):
        """Request (read) the current status of the given device sid."""
        self.send_command({"cmd": "read", "sid": device_sid})

    def update_rgb_color(self, r, g, b, a):
        cipher = AES.new(self.gatewayPassword, AES.MODE_CBC, self.IV)
        token = self.last_tokens[self.config.gatewayId]
        enc = cipher.encrypt(token)
        key = binascii.hexlify(enc).decode('ascii')
        color = (int(a) << 24)|(int(r) << 16)|(int(g) << 8)|b
        self.send_command({"cmd": "write", "model": "gateway", "sid": self.config.gatewayId, "short_id": 0, "data": {'rgb': color,'key': key.upper()}})

    def send_command(self, data):
        """Send a command to the UDP subject (all related will answer)."""
        self.socket.sendto(json.dumps(data).encode("utf-8"),
                           (self.MULTICAST_ADDRESS, self.MULTICAST_PORT))

    def get_nodes(self):
        """Return the current discovered node configuration."""
        return self.nodes