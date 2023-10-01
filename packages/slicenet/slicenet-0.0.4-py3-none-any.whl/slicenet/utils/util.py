class utilRatio:
    def __init__(self, value):
        """Initialize the object to its full value initially"""
        self.value = value
    
    def current(self, used: float) -> float:
        """Return the current utilization ratio as a factor of used value"""
        return (100 - abs((used/self.value)*100))
