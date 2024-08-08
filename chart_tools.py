from chart_xml_interface import *

SEQ_VER = 9

#question: do we really need this class?
class Beat:
    def __init__(self, value = 0: int, relativeTo = 0):
        self.value = 0
        if relativeTo is Beat:
            pass


#A 'size' for an individual note
class sizeUnit:
    def __init__(self, left_pos = 0, right_pos = 10000):
        self.left_pos = left_pos
        self.right_pos = right_pos


class Chart:
    #Either pass a chart root tag as xml.etree.ElementTree.Element, or pass no arguments and create an empty chart
    def __init__(self, xmlChart = None):
        if xmlChart is not None:
            self.xmlChart = xmlChart
        else:
            self.xmlChart = createEmptyChartXML()

    @property
    def timeUnit():
        return self.xmlChart.info.time_unit
    @timeUnit.setter
    def timeUnit(self, value):
        self.xmlChart.info.time_unit = value

    @property
    def steps():
        return self.xmlChart.sequenceDataTag


