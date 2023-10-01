import uuid
from slicenet.utils.slicenetlogger import slicenetLogger as logger

class Slicelet:
    def __init__(self, name: str, duration: float, service_id: uuid.UUID):
        self.id = uuid.uuid4()
        self.name = name
        self.slaViolation = False
        self.delaySeconds = 0 # We assume no delay initially
        self.duration = duration
        self.service_id = service_id
        self.eventHistory = {}
    
    def getName(self):
        return self.name
    
