import uuid
from slicenet.sliceMgr import SliceMgr
from slicenet.service import Service
from slicenet.slicelet import Slicelet
from slicenet.utils.slicenetlogger import slicenetLogger as logger
import concurrent.futures
import threading
import time
from time import strftime, localtime
from tabulate import tabulate

class ServiceMgr:

    services = {} #List of services
    slicelets = {} #List of slicelets
    traffic = [] #List of input slicelets awaiting to be processed

    def registerService(service: Service):
        """Register a given service object"""
        ServiceMgr.services[service.id] = service
        logger.info(f"Registered a Service {service.name}")
        logger.debug(f"Registered a Service {service.name} {service.id}")
    
    def unRegisterService(id: uuid.UUID):
        """Un Registered a given service by its id"""
        del ServiceMgr.services[id]
        logger.debug(f"Un Registered Service {id}")

    def deployServiceForSlicelet(slicelet: Slicelet):
        """Deploy a service for a given slicelet object"""
        service: Service = ServiceMgr.services[slicelet.service_id]
        for k,v in service.slices.items():
            SliceMgr.addService(k,v,slicelet.id) # Here we provide slicelet'd ID as the service instance ID
        ServiceMgr.slicelets[slicelet.id] = slicelet
        logger.info(f"Deployed slice under {service.name} for {slicelet.name}")
        logger.debug(f"Deployed slice under {service.name} {service.id} for {slicelet.name} {slicelet.id}")
    
    def unDeployServiceForSlicelet(slicelet_id: uuid.UUID):
        """Un Deploy a service for a given slicelet object"""
        slicelet : Slicelet = ServiceMgr.slicelets[slicelet_id]
        service: Service = ServiceMgr.services[slicelet.service_id]
        for k,_ in service.slices.items():
            SliceMgr.removeService(k, slicelet_id)
        #del ServiceMgr.slicelets[slicelet.id]
        logger.info(f"Un-Deployed slice under {service.name} for {slicelet.name}")
        logger.debug(f"Un-Deployed slice under {service.name} {service.id} for {slicelet.name} {slicelet.id}")
    
    def canAdmitSlicelet(slicelet: Slicelet) -> bool :
        """ Check whether a given slicelet object can be admitted"""
        service : Service = ServiceMgr.services[slicelet.service_id]
        for k,v in service.slices.items():
            if v/100 > SliceMgr.getSliceLoadLevelInfo(k):
                return False
        return True
    
    def processSlicelet(slicelet: Slicelet):
        logger.info(f"Spawned a new thread {threading.get_ident()} for {slicelet.getName()}")
        cannotExit = True
        slicelet_start_time = time.time()
        while cannotExit:
            if ServiceMgr.canAdmitSlicelet(slicelet):
                logger.info(f"Able to admit slicelet {slicelet.name}")
                ServiceMgr.deployServiceForSlicelet(slicelet)
                slicelet_actual_start_time = time.time()
                
                # Keep this slicelet alive for the required duration
                logger.info(f"Proceeding to sleep {slicelet.name} for {slicelet.duration} secs")
                time.sleep(slicelet.duration)
                logger.info(f"Done sleeping {slicelet.name}")
                slicelet_end_time = time.time()
                ServiceMgr.unDeployServiceForSlicelet(slicelet.id)
                slicelet_delay_time = slicelet_actual_start_time - slicelet_start_time

                #update slicelet statistics
                slicelet.delaySeconds = slicelet_delay_time
                if slicelet.delaySeconds > ServiceMgr.services[slicelet.service_id].slaThreshold :
                    slicelet.slaViolation = True
                slicelet.eventHistory = [
                    {
                        "Slicelet Started" : strftime('%Y-%m-%d %H:%M:%S', localtime(slicelet_actual_start_time)) 
                    },
                    {
                        "Slicelet Ended" : strftime('%Y-%m-%d %H:%M:%S', localtime(slicelet_end_time)) 
                    },
                    {
                        "Slicelet Delay" : slicelet_delay_time
                    }
                ]
                cannotExit = False
                logger.info(f"Exiting experiment for {slicelet.name}")

        # """
        # Algorithm:
        #     1. For each slicelet, Spawn a thread.
        #     2. Start SLA clock. Acquire a lock. If lock acquired, proceed
        #         2a. Try to admit it. 
        #             2a1. If the admission is allowed:
        #                 4a : End the SLA clock
        #                 4a : Deploy Service for that slicelet & release the lock
        #                 4b : Note down current time and start the clock
        #                 4c : Keep the service alive until slicelet duration.
        #                 4d : At the end of duration, Un Deploy Service
        #                 4e : For each of the milestone, note down the timeinstance inside slicelet events.
        #         5. If the admission is not allowed:
        #                 5a : Release the lock
        #                 5b : Try to acquire the lock
        #     4. After all slicelets have had their run, Dump the eventHistory of all slicelets
        # """

    
    def scheduleSlicelet(slicelet: Slicelet):
        ServiceMgr.traffic.append(slicelet)
    
    def displaySliceletStatistics():
        """Dump slice info statistics on std out."""
        headers = ["Slicelet ID", "Slicelet Name", "SLA Violation", "Event History"]
        items = []
        for k,v in ServiceMgr.slicelets.items():
            item = [str(k), v.name, str(v.slaViolation), str(v.eventHistory)]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))

    
    def launchExperiment():
        # Determine max threads needed
        workers = len(ServiceMgr.traffic)

        # Spawn a thread for each slicelet and wait for it to process
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            executor.map(ServiceMgr.processSlicelet, ServiceMgr.traffic)
        
        # Once the experiment is done, display the statistics
        ServiceMgr.displaySliceletStatistics()




