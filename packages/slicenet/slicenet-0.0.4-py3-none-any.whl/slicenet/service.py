import uuid
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from tabulate import tabulate

class Service:

    def __init__(self, name: str, priority: int=1):
        """Initialize the communication service object by its name and optional priority"""
        self.name = name
        self.priority = priority
        self.slaThreshold = 0 
        self.id = uuid.uuid4()
        self.slices = {} # these slices along with their weights make up this service
        logger.info(f"Creating a service {self.name}")
        logger.debug(f"Creating a service {self.name} {self.id} {self.priority}")

    def composeService(self, slice_id: uuid.UUID, weight: float, slaThreshold: float=10):
        """Compose a service by a slice and its corresponding weight"""
        self.slices[slice_id] = weight
        self.slaThreshold = slaThreshold # default 10 sec delay is acceptable
        logger.info(f"Composing service {self.name} with slice {slice_id} with weight {weight}% with a sla threshold of {slaThreshold} secs")

    def dumpServiceCompositionDetails(self):
        """Dump the service composition details std out"""
        headers = [f"Slice IDs under {self.name}", "Weightage(%)"]
        items = []
        for k,v in self.slices.items():
            item = [k, v]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))  

