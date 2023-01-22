import sys
from modules.config import Config, ConfigException
from modules.dataExtractor import DataExtractor
from modules.dataPrepare import DataPrepare


# from modules.tableData import TableData
# from modules.excelGenerator import ExcelGenerator



if __name__ == "__main__":

    try:
        config = Config()
        config.auditConfig()
    except ConfigException as ex:
        print(ex)
        sys.exit()

    parsedData = DataExtractor(config).getData()

    print("DEV :: Duplicate safeguard should be placed here...")
    
    groupedData = DataPrepare(parsedData, config)




# tableData = TableData("test", garmentData[0], config)

# excelGen = ExcelGenerator(tableData, config)
# excelGen.create()