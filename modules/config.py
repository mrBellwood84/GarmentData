import os, json

class Config():
    """
    Hold configuration values for application.
    Run auditConfig to check file and folder path
    """

    def __init__(self) -> None:

        configPath = os.path.join(os.getcwd(), "config.json")
        configExist = os.path.exists(configPath)

        if configExist:
            self.__readConfigFile(configPath)
            return

        self.__createAppFolders()
        self.__setDefaultConfig()
        self.__writeConfigFile(configPath)
        raise ConfigException("Configuration file created")

    def auditConfig(self):
        """
        Check files and folder paths provided by config file. 
        Will raise Config exception if paths or source files are missing.
        """

        sourceFolderExist = os.path.exists(self.sourceFolder)
        if not sourceFolderExist:
            raise ConfigException(f"Could not find source folder\n  Path: {self.sourceFolder}")

        outputFolderExist = os.path.exists(self.outputFolder)
        if not outputFolderExist:
            raise ConfigException(f"Could not find output folder\n  Path: {self.outputFolder}")

        if sourceFolderExist:
            files = os.listdir(self.sourceFolder)
            count = 0
            for file in files:
                postfix = file.split(".")[1]
                if postfix == "csv":
                    count += 1
            if count == 0:
                raise ConfigException(f"No .CSV files in source folder\n  Path: {self.sourceFolder}")

    def __createAppFolders(self):

        root = os.getcwd()
        
        sourceFolder = os.path.join(root, "Source")
        sourceFolderExist = os.path.exists(sourceFolder)

        outputFolder = os.path.join(root, "Output")
        outputFolderExist = os.path.exists(outputFolder)

        if not sourceFolderExist:
            os.mkdir(sourceFolder)
        if not outputFolderExist:
            os.mkdir(outputFolder)

    def __readConfigFile(self, path):

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.__dict__.update(data)
            
    def __writeConfigFile(self, path):

        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.__dict__, file, indent=4)

    def __setDefaultConfig(self):

        root = os.getcwd()

        self.sourceFolder = os.path.join(root, "Source")
        self.outputFolder = os.path.join(root, "Output")

        self.excelFile = os.path.join(self.outputFolder, "result.xlsx")

        self.csvDelimitor = ":"
        
        self.sizeKeys = ["XLITEN","LITEN","MEDIUM","STOR","XSTOR","2XSTOR","3XSTOR","4XSTOR","5XSTOR",]
        self.modelKeys = ["BUKSE","KITTEL","FRAKK","RØD KITTEL","BLÅ BUKSE","BLÅ KITTEL",]

        self.modelLabel = "MODELL"
        self.sizeLabel = "STØRRELSE"
        self.countLabel = "OPPLASTET"

        self.encodingCorrections = [
            ["ï¿½", "Ø"]
        ]

    def __requiredFoldersExist(self):
        sourceFolderExist = os.path.exists(self.sourceFolder)
        outputFolderExist = os.path.exists(self.outputFolder)
        return sourceFolderExist and outputFolderExist


class ConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)