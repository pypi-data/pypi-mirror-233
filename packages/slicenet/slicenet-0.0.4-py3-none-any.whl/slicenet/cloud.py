from slicenet.utils.util import utilRatio
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from slicenet.nf import Nf
import uuid
from typing import Dict
from readerwriterlock import rwlock

class Cloud():

    def __init__(self, ram: float, cpu: float, hdd: float, name: str='default', cat: str='edge'):
        """Initialize Cloud Object with ram, cpu, hdd items"""
        self.id = uuid.uuid4()
        self.ram = ram
        self.cpu = cpu
        self.hdd = hdd
        self.name = name
        self.cat = cat
        self.ramUtil = utilRatio(ram)
        self.cpuUtil = utilRatio(cpu)
        self.hddUtil = utilRatio(hdd)
        self.rcLock = rwlock.RWLockWrite()
        self.rcLock_r = self.rcLock.gen_rlock() # Reader lock for cloud capacity
        self.rcLock_w = self.rcLock.gen_wlock() # Writer lock for cloud capacity
        self.deployedNfs = []
        logger.info(f"Created a cloud object with {self.name}")
        logger.debug(f"Created a cloud object with {self.id} {self.cpu} {self.ram} {self.hdd} {self.cat}")

    def reserve(self, work: Nf):
        """Reserve cloud resources for a workload defined as Nf"""
        with self.rcLock_w:
            self.ram -= work.ram
            self.cpu -= work.cpu
            self.hdd -= work.hdd
            self.deployedNfs.append(work.id)
            logger.info(f"Reserved capacity for {work.name} from {self.name}")
    
    def tryAllocate(self, work: Nf) -> bool:
        """Try allocating a workload and see if there is enough room"""
        with self.rcLock_r:
            if work.ram > self.ram:
                logger.debug(f"""tryAllocate failed with {self.name} 
                            for {work.name}. Insufficent RAM!
                            """)
                return False
            if work.cpu > self.cpu:
                logger.debug(f"""tryAllocate failed with {self.name} 
                            for {work.name}. Insufficent CPU!
                            """)
                return False
            if work.hdd > self.hdd:
                logger.debug(f"""tryAllocate failed with {self.name} 
                            for {work.name}. Insufficent HDD!
                            """)
                return False
            
            return True
    
    def reclaim(self, work: Nf):
        """Reclaim cloud resources from the given workload given as Nf"""
        with self.rcLock_w:
            self.ram += work.ram
            self.cpu += work.cpu
            self.hdd += work.hdd
            self.deployedNfs.remove(work.id)
            logger.info(f"Reclaimed capacity allocated for {work.name} from {self.name}")

    def returnCurrentUtilDict(self) -> Dict[str, float]:
        """Return the current utilization ratio dict object"""
        with self.rcLock_r:
            rU = self.ramUtil.current(self.ram)
            cU = self.cpuUtil.current(self.cpu)
            hU = self.hddUtil.current(self.hdd)
            cloudUtilRatio = {}
            cloudUtilRatio['cpu'] = cU
            cloudUtilRatio['ram'] = rU
            cloudUtilRatio['hdd'] = hU
            logger.debug(f"Current util ratio {cloudUtilRatio}")
            return cloudUtilRatio
    
    def returnAvgCloudUtilRatio(self) -> float:
        """Return the average cloud utilization ratio"""
        with self.rcLock_r:
            rU = self.ramUtil.current(self.ram)
            cU = self.cpuUtil.current(self.cpu)
            hU = self.hddUtil.current(self.hdd)
            avg = (rU + cU + hU)/3
            logger.debug(f"Average Cloud utilization ratio {avg}")
            return avg        
    

if __name__ == '__main__':
    print(f"Testing Cloud Creation")
    mycloud = Cloud(1000, 10, 10000)
    myNf = Nf('Nf1', 343,6.7,9865)
    print(f"Trying to allocate work : {mycloud.tryAllocate(myNf)}")
    mycloud.reserve(myNf)
    uRatio = mycloud.returnCurrentUtilDict()
    print(f"The current cloud utilization:")
    print(f"RAM : {uRatio['ram']}%  CPU : {uRatio['cpu']}%  HDD : {uRatio['hdd']}%")
    mycloud.reclaim(myNf)
    uRatio = mycloud.returnCurrentUtilDict()
    print(f"The current cloud utilization:")
    print(f"RAM : {uRatio['ram']}%  CPU : {uRatio['cpu']}%  HDD : {uRatio['hdd']}%")   

