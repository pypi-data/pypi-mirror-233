import socket as so
import threading
import time
import copy
from queue import Queue
from queue import Empty

PING_INTERVAL = 1
BUFFER_SIZE = 4116

class AudioSocket:
    def __init__(self, sockSend=None, sockRecv=None):
        if sockSend is None:
            self.sockSend = so.socket(so.AF_INET, so.SOCK_DGRAM)
        else:
            self.sockSend = sockSend
        
        if sockRecv is None:
            self.sockRecv = so.socket(so.AF_INET, so.SOCK_DGRAM)
        else:
            self.sockRecv = sockRecv

        self.audioQueue = Queue()
        self.threadAudioRecv = None
        self.threadMsgSend = None
        self.lost_conection = True

        self.host = None
        self.port = None

    def __del__(self):
        self.disconnect()

    def get_audio(self):
        if not self.lost_conection:
            try:
                audioPacket = copy.copy(self.audioQueue.get(True, 1))
            except Empty:
                return None
            if not audioPacket is None:
                sound_data, timestamp, sync = audioPacket
                return sound_data, timestamp, sync
            else:
                return None
        else:
            return None
    
    def sync_audio(self):
        if not self.lost_conection and not self.audioQueue is None:
            self.audioQueue = Queue()

    def receive_audio(self):
        MAX_TRIES = 5
        tries = MAX_TRIES
        while not self.lost_conection:
            if tries <= 0:
                self.lost_conection = True
                break
            try:
                audioPacket = self.myreceive()
                tries = MAX_TRIES
                self.audioQueue.put(copy.copy(audioPacket))
            except so.timeout:
                tries -= 1

    def send_ping(self):
        while not self.lost_conection:
            self._send_message("PING")
            time.sleep(PING_INTERVAL)

    def _send_message(self, message):
        if self.host != None and self.port != None:
            server_address = (self.host, self.port)
            self.sockSend.sendto(message.encode(), server_address)

    def start_audio_thread(self):
        self.threadAudioRecv = threading.Thread(target=self.receive_audio)
        self.threadAudioRecv.start()
    
    def start_ping_thread(self):
        self.threadMsgSend = threading.Thread(target=self.send_ping)
        self.threadMsgSend.start()

    def connect(self, host, port):
        MAX_TRIES = 5
        self.host = host
        self.port = port
        self.sockRecv.bind(("", self.port))
        self.sockRecv.settimeout(1)
        self._send_message("CONNECT-AUDIO")
        tries = MAX_TRIES
        while True:
            print(f"Connecting to {self.host}:{self.port}...")
            if tries <= 0:
                break
            try:
                data, _ = self.sockRecv.recvfrom(BUFFER_SIZE)
                if not data is None:
                    print("Succesfully connected")
                    self.lost_conection = False
                    break
            except so.timeout:
                tries -= 1
        return not self.lost_conection

    def disconnect(self):
        if not self.lost_conection:
            self._send_message("DISCONNECT-AUDIO")
        self.host = None
        self.port = None
        self.lost_conection = True
        self.sockRecv.detach()
        if (self.threadAudioRecv != None):
            self.threadAudioRecv.join()
        if (self.threadAudioRecv != None):
            self.threadMsgSend.join()

    def myreceive(self):
        try:
            data, _ = self.sockRecv.recvfrom(BUFFER_SIZE)
            return ((data[:-16], int.from_bytes(data[-16:-8], "big", signed=False), int.from_bytes(data[-8:], "big", signed=False)))
        except so.timeout:
            raise so.timeout