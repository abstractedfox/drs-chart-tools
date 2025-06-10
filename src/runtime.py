from chart_tools_new import *
import uuid

class LogLevel(Enum):
    BASIC = 0
    WARNING = 1
    ERROR = 2
    DEBUG = 3

def load_from_file(path):
    return chartRootXML(xml.etree.ElementTree.parse(path))

def log(string, level = LogLevel.BASIC):
    print(string)

class Session:
    def __init__(self, path):
        self.path = path
        self.chart_instance = None
        self.ID = uuid.uuid4().hex #str

        try:
            self.chart_instance = load_from_file(path)
        except FileNotFoundError:
            log("Could not find file {}, a new chart will be created on save.".format(path), LogLevel.WARNING)
            self.chart_instance = chartRootXML(createEmptyChartXML())

    def save(self):
        return save_chart(self.chart_instance, self.path) 

    
