from robobopy_audiostream.audiosocket import AudioSocket

class RoboboAudio:
    def __init__(self, ip, robot_id=0):
        self.port = 40406 + (robot_id * 10)
        self.ip = ip
        self.socket = AudioSocket()

    def connect(self):
        if (self.socket.connect(self.ip, self.port)):
            self.socket.start_audio_thread()
            self.socket.start_ping_thread()
        else:
            print("Can't connect to server")
            
    def _getAudioAux(self):
        if not self.socket.lost_conection:
            packet = self.socket.get_audio()
            if packet is None:
                self.disconnect()
            else:
                return packet
        else:
            print("Please connect to the server")

    def getAudioBytes(self):
        if not self.socket.lost_conection:
            audioPacket = self._getAudioAux()
            if not audioPacket is None:
                raw_audio, ts, snc = self._getAudioAux()
                return raw_audio
            else:
                return None
        else:
            print("Please connect to the server")
        
    def getAudioWithMetadata(self):
        if not self.socket.lost_conection:
            audioPacket = self._getAudioAux()
            if not audioPacket is None:
                raw_audio, ts, snc = self._getAudioAux()
                return raw_audio, ts, snc
            else:
                return None
        else:
            print("Please connect to the server")

    def syncAudioQueue(self):
        if not self.socket.lost_conection:
            self.socket.sync_audio()
        else:
            print("Please connect to the server")
    
    def disconnect(self):
        self.socket.disconnect()