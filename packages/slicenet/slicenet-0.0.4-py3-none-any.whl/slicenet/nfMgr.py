from slicenet.cloud import Cloud
from slicenet.nf import Nf
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from tabulate import tabulate
import uuid
from typing import Dict

class NfMgr():
    
    clouds = {}
    schedular = None
    nfs = {}
    # nfSlicesMap = {} not used
    nfCloudMap = {}
    
    def registerCloud(c: Cloud):
        """Register a cloud object with this NF manager"""
        NfMgr.clouds[c.id] = c
        logger.info(f"Registering Cloud {c.name}")
        logger.debug(f"Registering Cloud {c.name} with ID {c.id}")

    def deregisterCloud(id: uuid.UUID):
        """De-Register this cloud (as pointed by this id) from this NF Manager""" 
        del(NfMgr.clouds[id])
        logger.debug(f"De-Registering Cloud {id}")
    
    def checkAvailablity(c: Cloud, w: Nf) -> bool:
        """Check whether a given workload (Nf) can be scheduled in the Cloud"""
        return c.tryAllocate(w)
    
    def setSchedularPolicy(policy: str):
        """Set the schedular policy for cloud selection"""
        if policy == 'first-available-method':
            NfMgr.schedular = NfMgr.firstAvailablePolicy
            logger.info(f"Setting the schedular policy for cloud selection to {policy}")

    def addSlice(id: uuid.UUID, weightage: float, slice_id: uuid.UUID):
        """Add a slice with its id, weightage to a Nf by its id"""
        logger.info(f"Adding slice for {id} using weight {weightage}%")
        n = NfMgr.nfs[id]
        n.addSlice(weightage/100, slice_id)
    
    def removeSlice(id: uuid.UUID, slice_id: uuid.UUID):
        """Remove a slice by its id on a NF by its id"""
        logger.debug(f"Removing a slice {slice_id} from {id}")
        n = NfMgr.nfs[id]
        n.removeSlice(slice_id)

    def deployNf(w: Nf) -> bool:
        """Deploy a given Nf object and return the status"""
        c = NfMgr.schedular(w)
        if c == None:
            logger.info(f"Unable to accommodate {w.name}")
            return False
        c.reserve(w)
        NfMgr.nfs[w.id] = w
        NfMgr.nfCloudMap[w.id] = c.id
        logger.info(f"Deployed {w.name} in {c.name}")
        logger.debug(f"Deployed {w.name} {w.id} in {c.name} {c.id}")
        return True
    
    def unDeployNf(id: uuid.UUID):
        """Un Deploy a given NF by its ID"""
        cld_id = NfMgr.nfCloudMap[id]
        NfMgr.clouds[cld_id].reclaim(NfMgr.nfs[id])
        del(NfMgr.nfs[id])
        del(NfMgr.nfCloudMap[id])
        logger.debug(f"UnDeployed {id}")

    def firstAvailablePolicy(work: Nf) -> Cloud:
        """Return the best suitable cloud by applying the firstAvailablePolicy method"""
        logger.debug(f"Applying First Available Policy method to find a suitable cloud for {work.name}")
        for c in NfMgr.clouds.values():
            if NfMgr.checkAvailablity(c,work):
                logger.info(f"Selected {c.name} to accomodate {work.name}")
                return c
        logger.info(f"Unable to find a suitable cloud to accomodate {work.name}")
        return None
    
    def getCloudUtilRatio(id: uuid.UUID) -> Dict[str, float]:
        """Return the cloud util ratio of a given cloud by its id"""
        c = NfMgr.clouds[id]
        logger.debug(f"Current Cloud utilization ratio for {c.name} is {c.returnCurrentUtilDict()}")
        return c.returnCurrentUtilDict()

    def dumpCloudInfo():
        """Dump the cloud info statistics on std out"""
        headers = ["Cloud ID", "Name", "RAM(%)", "CPU(%)", "HDD(%)"]
        items = []
        for c in NfMgr.clouds.values():
            u = c.returnCurrentUtilDict()
            item = [c.id, c.name, u['ram'], u['cpu'], u['hdd']]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))

    def dumpNfInfo():
        """Dump the Nf info statistics on std out"""
        #headers = ["Cloud Name", "NF ID", "NF Name", "Available Slices", "Slice Util Ratio %"]
        headers = ["Cloud Name", "NF ID", "NF Name", "Overall Util Ratio %"]
        items = []
        for k,v in NfMgr.nfCloudMap.items():
            item = [NfMgr.clouds[v].name ,k, NfMgr.nfs[k].name, 
                   # NfMgr.nfs[k].getSliceCount(), NfMgr.nfs[k].getSliceUtilRatio()]
                   NfMgr.nfs[k].getNfUtilRatio()]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))

    def dumpNfInfoSliceDetails():
        """Dump the slice info statistics on std out"""
        headers = ["Cloud Name", "NF ID", "NF Name", "Overall Utilization Ratio %"]
        items = []
        for k,v in NfMgr.nfCloudMap.items():
            item = [NfMgr.clouds[v].name ,k, NfMgr.nfs[k].name, 
                   NfMgr.nfs[k].getNfUtilRatio()]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))            


if __name__ == '__main__':
    print("Testing Cloud Mgr")
    c1 = Cloud(1000, 10, 10000, name="c1")
    c2 = Cloud(2000, 20, 20000, name="c2")
    nf1 = Nf(name='nf1', ram=100, cpu=9, hdd=1234)
    nf2 = Nf(name='nf2', ram=2200, cpu=1, hdd=1234)
    nf3 = Nf(name='nf3', ram=200, cpu=3, hdd=1234)
    NfMgr.setSchedularPolicy('first-available-method')
    NfMgr.registerCloud(c1)
    NfMgr.registerCloud(c2)
    #NfMgr.dumpCloudInfo()
    #NfMgr.deregisterCloud(c2.id)
    #NfMgr.dumpCloudInfo()
    d1 = NfMgr.deployNf(nf1)
    d2 = NfMgr.deployNf(nf2)
    d3 = NfMgr.deployNf(nf3)
    print(f"After Deployment")
    NfMgr.dumpCloudInfo()
    NfMgr.dumpNfInfo()
    if d1:
        NfMgr.unDeployNf(nf1.id)
    if d2:
        NfMgr.unDeployNf(nf2.id)

    print(f"After Un-Deployment")
    NfMgr.dumpCloudInfo()
    NfMgr.dumpNfInfo()
    

