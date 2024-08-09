from chart_xml_interface import *
from enum import Enum


SEQ_VER = 9
type ticks = int

class StepTypes(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    JUMP = 4

#question: do we really need this class?
class Beat:
    def __init__(self, value = 0: int, relativeTo = 0):
        self.value = 0
        if relativeTo is Beat:
            pass

#Literal coordinates for a note
class noteCoordinates:
    left_pos = 0
    right_pos = 0

    @property
    def MAX():
        return 65536

    @property
    def MIN():
        return 0

#A 'size' for an individual note
class sizeUnit:
    def __init__(self, size = 10000):
        self.size = size

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

    def addNote(self, noteSize: sizeUnit, position: noteCoordinates, time: ticks):
        newStep = XMLstep(createEmptyStepXML())
        newStep.start_tick = time
        newStep.end_tick = time
        newStep.left_pos = noteSize.left_pos
        newStep.right_pos = noteSize.right_pos
        #newStep.kind =


#Get the literal coordinates of a note of size 'noteSize' at coordinate 'position' relative to 'relativeTo' (left or right)
#Returns None if the note would be out of bounds
def getPosition(noteSize: sizeUnit, position = 0, relativeTo = 'L') -> noteCoordinates | None:
    result = noteCoordinates()
    if position == 'L':
        result.left_pos = position
        result.right_pos = position + sizeUnit.size

        if result.right_pos > noteCoordinates.MAX or result.left_pos < noteCoordinates.MIN:
            return None
    else if position == 'R':
        result.left_pos = noteCoordiantes.MAX - position - sizeUnit.size
        result.right_pos = noteCoordinates.MAX - position

        if result.right_pos > noteCoordinates.MAX or result.left_pos < noteCoordinates.MIN:
            return None
    else:
        return None

    return result
