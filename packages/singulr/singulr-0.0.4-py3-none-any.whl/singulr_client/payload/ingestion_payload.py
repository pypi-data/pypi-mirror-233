# Created by msinghal at 19/09/23
import time
class IngestionData:
    def __init__(self, id, payload):
        self.id = id
        self.source = "source-1"
        self.source_type = "LANG_CHAIN"
        self.timestamp = int(time.time() * 1000)
        self.type = "TRACE"
        self.serialization_type = "JSON"
        self.payload = payload


    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "type": self.type,
            "serialization_type": self.serialization_type,
            "payload": self.payload
        }
