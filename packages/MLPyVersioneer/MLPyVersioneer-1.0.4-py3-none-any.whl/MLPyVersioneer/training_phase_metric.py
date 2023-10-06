

class TrainingPhaseMetric():
    """
    Class to store training phase metric
    """

    def __init__(self, name, value, epoch) -> None:
        self.epoch = epoch
        self.name = name
        self.value = value

    def __str__(self):
        return  f"Epoch: {self.epoch}, Name: {self.name}, Value: {self.value}"
    
    def __json__(self):
        return dict(epoch=self.epoch, name=self.name, value=self.value)
    
    
    