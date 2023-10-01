from slicenet.nfMgr import NfMgr
from tabulate import tabulate
from slicenet.staticslice import StaticSlice
from slicenet.utils.slicenetlogger import slicenetLogger as logger
import uuid

class SliceMgr():
    
    slices = {}
    # sliceSvcsMap = {} not used

    def deploySlice(slice: StaticSlice):
        """Deploy a StaticSlice Object"""
        logger.info(f"Deploying slice {slice.name}")
        logger.debug(f"Deploying slice {slice.name} {slice.id}")
        for k,v in slice.sliceNfs.items():
            NfMgr.addSlice(k, v, slice.id)
        SliceMgr.slices[slice.id] = slice
    
    def unDeploySlice(id: uuid.UUID):
        """UnDeploy a StaticSlice identified by its Id"""
        logger.debug(f"Un-Deploying slice {id}")
        slice = SliceMgr.slices[id]
        for k,_ in slice.sliceNfs.items():
            NfMgr.removeSlice(k)
        del(SliceMgr.slices[id])
    
    def addService(slice_id: uuid.UUID, weightage: float, service_id: uuid.UUID):
        """Add a service identified by service_id to a slice identifed with slice_id for a weightage"""
        logger.info(f"Adding service for slice {slice_id} using weight {weightage}")
        logger.debug(f"Adding service {service_id} for slice {slice_id} using weight {weightage}")
        s: StaticSlice = SliceMgr.slices[slice_id]
        s.addService(weightage/100, service_id)
    
    def removeService(slice_id: uuid.UUID, service_id: uuid.UUID):
        """Remove a service identified by service_id from a slice identified by slice_id"""
        s : StaticSlice = SliceMgr.slices[slice_id]
        s.removeService(service_id)
        logger.debug(f"Removing service {service_id} from {slice_id}")
    
    def getSliceLoadLevelInfo(slice_id: uuid.UUID):
        """Return the current slice utilization ratio for given slice object"""
        a_slice : StaticSlice = SliceMgr.slices[slice_id]
        return a_slice.getSliceRemainingCapacity()

    def dumpSlices():
        """Dump slice info statistics on std out."""
        headers = ["Slice ID", "Slice Name", "Slice Availablity (%)"]
        items = []
        for k,v in SliceMgr.slices.items():
            item = [k,v.name, 100 - v.getSliceUtilRatio()]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))