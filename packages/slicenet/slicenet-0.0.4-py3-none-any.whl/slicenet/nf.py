import uuid
from slicenet.utils.util import utilRatio
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from readerwriterlock import rwlock

class Nf():
    
    def __init__(self, name: str, ram :float, cpu :float, hdd :float, initCapacity: int =1):
        """ Initialize Nf object with name, ram, cpu, hdd capacity"""
        self.id = uuid.uuid4()
        self.name = name
        self.ram = ram
        self.cpu = cpu
        self.hdd = hdd
        self.remainingCapacity = initCapacity
        self.rcLock = rwlock.RWLockWrite()
        self.rcLock_r = self.rcLock.gen_rlock() # Reader lock for self.remainingCapacity
        self.rcLock_w = self.rcLock.gen_wlock() # Writer lock for self.remainingCapacity
        self.sliceUtilRatio = utilRatio(initCapacity)
        self.slices = {}
        logger.info(f"Created a NF with NAME {self.name}")
        logger.debug(f"Created a NF with ID {self.id} RAM {self.ram} CPU {self.cpu} HDD {self.hdd}")
    
    def addSlice(self, weight: float, slice_id: uuid):
        """Given the weightage and slice id, add this slice into the NF's resources"""
        with self.rcLock_w:
            self.remainingCapacity -= 1 * weight
            logger.debug(f"{self.name}'s remaining capacity {self.remainingCapacity * 100}%")
        self.slices[slice_id] = weight
        logger.info(f"Adding a slice {slice_id} to {self.name} reserving {weight * 100}% capacity")
    
    def removeSlice(self, slice_id: uuid):
        """Given the slice id, remove the slice from the current NF resource"""
        with self.rcLock_w:
            self.remainingCapacity += 1 * self.slices[slice_id]
            logger.debug(f"{self.name}'s remaining capacity {self.remainingCapacity * 100}%")
        del self.slices[slice_id]
        logger.info(f"Removing a slice {slice_id} from {self.name}")
    
    def trySlice(self, weight: float) -> bool:
        """See whether this NF object can accomdate given slice as a factor if NF resource weight""" 
        with self.rcLock_r:
            return self.remainingCapacity > weight
    
    def getRemainingCapacity(self) -> int:
        """Return the remaining capacity of this NF"""
        with self.rcLock_r:
            return self.remainingCapacity
    
    def getNfUtilRatio(self) -> any:
        """Return the total utilization ratio of this NF as consumed by slices"""
        with self.rcLock_r:
            return self.sliceUtilRatio.current(self.remainingCapacity)