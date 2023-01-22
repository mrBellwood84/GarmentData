from datetime import date

class GarmentData:
    
    model: str = None
    size: str  = None
    count: int = None

    def __str__(self) -> str:
        return f"Model: {self.model}, Size: {self.size}, Count: {self.count}"


class MachineData:

    machineName: str
    location: str

    def __init__(self) -> None:
        self.garmentData: list[GarmentData] = []

    def setDates(self, startDate: date, endDate: date):
        self.startDate: date = startDate
        self.endDate: date  = endDate
        self.week: int = self.startDate.isocalendar().week
    
    def appendGarmentData(self, data: GarmentData):
        self.garmentData.append(data)

    def __str__(self) -> str:
        return f"""
    Machine: {self.machineName} | Location: {self.location}
    StartDate: {self.startDate} | EndDate: {self.endDate} | Weeknumber: {self.week} 
    Garment data count: {len(self.garmentData)}
    """

class DataGroup:

    def __init__(self, weekNumber, location) -> None:

        self.week: int = weekNumber
        self.location: str = location
        self.machineData: list[MachineData] = []
        self.table = None

    def appendMachineData(self, data: MachineData):
        self.machineData.append(data)
    
    def __str__(self) -> str:
        return f"""
    Location: {self.location} | Week: {self.week}
    Item count: {len(self.machineData)}
    """

    
