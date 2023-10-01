import uuid
from slicenet.utils.util import utilRatio
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from readerwriterlock import rwlock

class StaticSlice():

    def __init__(self, name: str, priority: int=1, initCapacity: int=1):
        """Initialize a StaticSlice Object with name, optional priority and capacity"""
        self.id = uuid.uuid4()
        self.name = name
        self.sliceNfs = {} # these NFs along with their weights make up this slice
        self.slicePriority = priority
        self.remainingCapacity = initCapacity
        self.rcLock = rwlock.RWLockWrite()
        self.rcLock_r = self.rcLock.gen_rlock() # Reader lock for self.remainingCapacity
        self.rcLock_w = self.rcLock.gen_wlock() # Writer lock for self.remainingCapacity
        self.services = {} # this slice powers these services
        self.sliceUtilRatio = utilRatio(initCapacity) #at start 100% of slice is available
        logger.info(f"Creating a static slice {self.name}")
        logger.debug(f"Creating a static slice {self.name} {self.id} {self.slicePriority}")
    
    def composeSlice(self, nf_id: uuid.UUID, weight: float):
        """Compose a slice by a NF's weightage identified by its id"""
        self.sliceNfs[nf_id] = weight
        logger.debug(f"Composing slice {self.name} with NF {nf_id} with weight {weight * 100}%")
    
    def addService(self, weight: float, service_id: uuid.UUID):
        """Add a Service on a given slice by its service_id and corresponding weightage"""
        with self.rcLock_w:
            self.remainingCapacity -= 1 * weight
            logger.debug(f"Remaining Slice Capacity {self.remainingCapacity * 100}%")
        self.services[service_id] = weight
        logger.debug(f"Adding service {service_id} to {self.name} with weight {weight * 100}%")
        
    
    def removeService(self, service_id: uuid.UUID):
        """Remove a service identified by its ID from this slice object"""
        with self.rcLock_w:
            self.remainingCapacity += 1 * self.services[service_id]
            logger.debug(f"Remaining Slice Capacity {self.remainingCapacity * 100}%")
        del self.services[service_id]
        logger.debug(f"Removing service {service_id} from {self.name}")
        
    
    def tryService(self, weight: float) -> bool:
        """Check if this slice object can accomadate a service"""
        with self.rcLock_r:
            return self.remainingCapacity > 1 * weight
    
    def getSliceRemainingCapacity(self) -> float:
        """Get the Slice's remaining capacity as a factor of utilization ratio"""
        with self.rcLock_r:
            return self.remainingCapacity
    
    def getSliceUtilRatio(self) -> float:
        """Get Slice Utilization ratio"""
        with self.rcLock_r:
            return self.sliceUtilRatio.current(self.remainingCapacity)