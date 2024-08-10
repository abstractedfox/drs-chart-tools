from chart_xml_interface import *
from enum import Enum
from decimal import *
import math


SEQ_VER = 9
#type Ticks = int
#type Beats = Decimal
Ticks = int
Beats = Decimal


beatSegments = {
        1: Beats(1),
        2: Beats(1) / Beats(2),
        3: Beats(1) / Beats(3),
        4: Beats(1) / Beats(4),
        6: Beats(1) / Beats(6),
        8: Beats(1) / Beats(8),
        12: Beats(1) / Beats(12),
        16: Beats(1) / Beats(16),
        24: Beats(1) / Beats(24),
        32: Beats(1) / Beats(32),
        64: Beats(1) / Beats(64)
    }

class StepTypes(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    JUMP = 4

class PlayerID(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    JUMPDOWN = 4

#question: do we really need this class?
class Beat:
    def __init__(self, value = 0, relativeTo = 0):
        self.value = 0
        if relativeTo is Beat:
            pass


class BPM:
    def __init__(self, bpm: int, bpmDecimals = 0, timeSigDenomi = 4, timeSigNum = 4):
        self.bpm = bpm
        self.bpmDecimals = bpmDecimals
        self.timeSigDenomi = timeSigDenomi
        self.timeSigNum = timeSigNum

    #BPMs are formatted in the XML such that the last two digits are the tenths and hundredths places
    def getBPMFormatted(self):
        if self.bpmDecimals < 10:
            return (str(self.bpm) + "0" + str(self.bpmDecimals))

        return (str(self.bpm) + str(self.bpmDecimals))


#Literal coordinates for a note
class noteCoordinates:
    MAX = 65536
    MIN = 0

    def __init__(self):
        self.left = int(0)
        self.right = int(0)
    #left_pos = 0
    #right_pos = 0

    @property
    def left_pos(self):
        return self.left
    @left_pos.setter
    def left_pos(self, value):
        self.left = int(value)

    @property
    def right_pos(self):
        return self.right
    @right_pos.setter
    def right_pos(self, value):
        self.right = int(value)



#A 'size' for an individual note
#class sizeUnit:
#    def __init__(self, size = 10000):
#        self.size = size
sizeUnit = int

def beatsToTicks(beats: Beats, timeUnit: Ticks):
    return int(math.floor(timeUnit * beats))


class Chart:
    #Either pass a chart root tag as xml.etree.ElementTree.Element, or pass no arguments and create an empty chart
    def __init__(self, xmlChart = None, timeUnit = Ticks(480), endTick = Ticks(0)):
        if xmlChart is not None:
            self.xmlChart = chartRootXML(xmlChart)
        else:
            self.xmlChart = chartRootXML(createEmptyChartXML())

        self.xmlChart.info.time_unit = timeUnit
        self.xmlChart.info.end_tick = endTick

    @property
    def timeUnit(self):
        return self.xmlChart.info.time_unit
    @timeUnit.setter
    def timeUnit(self, value):
        self.xmlChart.info.time_unit = value

    @property
    def steps():
        return self.xmlChart.sequenceDataTag

    def addBPM(self, bpm: BPM, time: Ticks):
        newBPM = XMLbpm(createEmptyBPMXML())
        newBPM.tick = time
        newBPM.bpm = bpm.getBPMFormatted()

        newMeasure = XMLmeasure(createEmptyMeasureXML())
        newMeasure.tick = time
        newMeasure.num = bpm.timeSigNum
        newMeasure.denomi = bpm.timeSigDenomi

        self.xmlChart.info.bpm_info.append(newBPM)
        self.xmlChart.info.measure_info.append(newMeasure)

    def addNote(self, noteSize: sizeUnit, position: noteCoordinates, time: Beats, playerID: PlayerID):
        time = beatsToTicks(time, self.timeUnit)
        newStep = XMLstep(createEmptyStepXML())
        newStep.start_tick = time
        newStep.end_tick = time
        newStep.left_pos = position.left_pos
        newStep.right_pos = position.right_pos
        newStep.kind = StepTypes.LEFT.value
        newStep.player_id = playerID.value

        self.xmlChart.sequence_data.append(newStep)

    def save(self, filename: str):
        self.xmlChart.write(filename)


#Get the literal coordinates of a note of size 'noteSize' at coordinate 'position' relative to 'relativeTo' (left or right)
#Returns None if the note would be out of bounds
def getPosition(noteSize: sizeUnit, position: int, relativeTo = 'L') -> noteCoordinates | None:
    result = noteCoordinates()

    if relativeTo == 'L':
        result.left_pos = position
        result.right_pos = position + noteSize

        if result.right_pos > noteCoordinates.MAX or result.left_pos < noteCoordinates.MIN:
            print("Note out of bounds " + str(result.left_pos) + " " + str(result.right_pos) + " position = " + str(position) + " " + relativeTo)
            return None
    elif relativeTo == 'R':
        result.left_pos = noteCoordiantes.MAX - position - noteSize
        result.right_pos = noteCoordinates.MAX - position

        if result.right_pos > noteCoordinates.MAX or result.left_pos < noteCoordinates.MIN:
            print("Note out of bounds " + str(result.left_pos) + " " + str(result.right_pos) + " position = " + str(position) + " " + relativeTo)
            return None
    else:
        print("Note out of bounds or invalid relative position " + str(result.left_pos) + " " + str(result.right_pos) + " position = " + str(position) + " " + relativeTo)
        return None

    return result
