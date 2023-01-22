from modules.config import Config
from modules.models import MachineData, DataGroup


class DataPrepare:

    def __init__(self, parsedData: list[MachineData], config: Config) -> None:

        self.config = config

        self.data = parsedData
        self.grouped = self.__group_data()
        self.__create_group_tabled_data()

    def __group_data(self) -> list[DataGroup]:

        sorted_data: list[DataGroup] = []

        for data in self.data:
            index = -1
            for i,v in enumerate(sorted_data):
                if v.location == data.location and v.week == data.week:
                    index = i
                    break
            
            if index == -1:
                dataGroup = DataGroup(data.week, data.location)
                dataGroup.appendMachineData(data)
                sorted_data.append(dataGroup)
                continue

            sorted_data[index].appendMachineData(data)

        return sorted_data

    def __create_group_tabled_data(self):
        for data in self.grouped:
            tables = self.__create_table_data(data.machineData)

            if len(tables) > 1:
                table = self.__concat_tables(tables)
            elif len(table) == 1:
                table = tables[0]
            else:
                return

            table = self.__remove_empty_rows(table)

            data.table = table

    def __create_table_data(self, data: list[MachineData]):

        result = []
        
        for d in data:
            
            headRow = [""] + self.config.sizeKeys
            contentRows = [[label] + [0 for _ in range(len(headRow) - 1)] for label in self.config.modelKeys]

            for garment in d.garmentData:
                
                modelIndex = None
                sizeIndex = headRow.index(garment.size)

                for i,v in enumerate(contentRows):
                    if v[0] == garment.model:
                        modelIndex = i
                        break
                
                contentRows[modelIndex][sizeIndex] = garment.count
            
            t = [headRow] + contentRows
            result.append(t)
        return result

    def __concat_tables(self, tables: list[list[list]]) -> list[list]:

        headRow = [""] + self.config.sizeKeys
        contentRows = [[label] + [0 for _ in range(len(headRow) - 1)] for label in self.config.modelKeys]

        for i,v in enumerate(contentRows):
            for j,_ in enumerate(v):
                if j == 0:
                    continue
                sum = 0
                for t in tables:
                    sum += t[i+1][j]
                contentRows[i][j] = sum
        
        return [headRow] + contentRows

    def __remove_empty_rows(self, table: list[list]) -> list[list]:

        copy = []
        
        for i,v in enumerate(table):
            if i == 0:
                copy.append(v)
                continue
            s = sum(v[1:])
            if s > 0:
                copy.append(v)
        
        return copy


            
