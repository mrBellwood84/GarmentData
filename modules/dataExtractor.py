import os, csv
from datetime import date
from modules.config import Config
from modules.models import GarmentData, MachineData
from modules.utils import normalize

class DataExtractor:

    def __init__(self, config: Config) -> None:

        self.config = config
        self.csvFiles = self.__getCsvFiles()

    def getData(self):
        rawData = self.__extractRawData()
        return self.__parseRawData(rawData)

    def __getCsvFiles(self) -> list[str]:

        folderContent = os.listdir(self.config.sourceFolder)
        csvFiles = []

        for file in folderContent:
            postfix = file.split(".")[1]
            if postfix == "csv":
                csvFiles.append(file)
        
        csvFiles = [os.path.join(self.config.sourceFolder, file) for file in csvFiles]
        return csvFiles
    
    def __extractRawData(self) -> list[list[list[str]]]:

        data = []

        for path in self.csvFiles:
            with open(path, "r") as file:
                reader = csv.reader(file, delimiter=self.config.csvDelimitor)
                content = [row[0].split("\t") for row in reader]
                data.append(content)
        return data
    
    def __parseRawData(self, data: list[list[list[str]]]) -> list[MachineData]:

        result = []

        for item in data:

            for i, v1 in enumerate(item):
                for j,v2 in enumerate(v1):
                    item[i][j] = normalize(v2, self.config.encodingCorrections)

            machineData = MachineData()

            machineInfo = item[3][8].split(" ")
            machineData.machineName = machineInfo[0]
            machineData.location = " ".join(machineInfo[1:])

            startDateStrList = item[1][8].split(".")
            endDateStrList = item[1][11].split(".")

            startDate = date(
                int(startDateStrList[2]), 
                int(startDateStrList[1]), 
                int(startDateStrList[0]) )

            endDate = date(
                int(endDateStrList[2]),
                int(endDateStrList[1]),
                int(endDateStrList[0]) )
            
            machineData.setDates(startDate, endDate)

            labels = item[4]
            garments = item[5:len(item)-2:2]

            for g in garments:

                garmentData = GarmentData()

                for index, value in enumerate(g):
                    label = labels[index]

                    if label == self.config.modelLabel:
                        garmentData.model = value.strip(" ")
                        continue

                    if label == self.config.sizeLabel:
                        garmentData.size = value.strip(" ")
                        continue

                    if label == self.config.countLabel:
                        garmentData.count = int(value)
                        break
                
                machineData.appendGarmentData(garmentData)
            
            result.append(machineData)
        
        return result
                