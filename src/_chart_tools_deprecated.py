#This file has been deprecated!
#For now it's still necessary for some unit tests that use it to generate test charts, but don't use it for anything new

from chart_xml_interface import *
from common import *

from enum import Enum
from decimal import *
import math
import io


SEQ_VER = 9
Ticks = int
Beats = Decimal

#for scripting charts in python
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

#Known good values for <extend><layer_name>
#the actual layer_name: [the associated "kind" that tends to go with it, a description, value for <id>]
layerNameValues = {
    "sp3_eff01": ["OverEffect", "Fiery explosion", 1],
    "sp3_eff02": ["OverEffect", "Explodey explosion", 2],
    "sp3_eff03": ["OverEffect", "Shake", 3],
    "sp3_led_01": ["Background", "", 1],
    "sp3_led_02": ["Background", "", 2],
    "sp3_led_03": ["Background", "", 3],
    "sp3_led_04": ["Background", "", 4],
    "sp3_led_05": ["Background", "", 5],
    "sp3_led_06": ["Background", "", 6],
    "sp3_led_07": ["Background", "", 7],
    "sp3_led_08": ["Background", "", 8],
    "sp3_led_09": ["Background", "", 9],
    "sp3_led_10": ["Background", "", 10],
    "sp3_led_11": ["Background", "", 11],
    "sp3_led_12": ["Background", "", 12],
    "sp3_eff01_b01": ["MiddleEffect", "", 1],
    "sp3_eff01_b02": ["MiddleEffect", "", 2],
    "sp3_eff03_b01": ["MiddleEffect", "", 3],
    "sp3_eff03_b02": ["MiddleEffect", "", 4],
    "sp3_eff03_b03": ["MiddleEffect", "", 4]
}

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


sizeUnit = int


def beatsToTicks(beats: Beats, timeUnit: Ticks):
    return int(math.floor(timeUnit * beats))

#Get the tick of the last element in a step
def getLastTimeInStep(step: stepXML) -> Ticks:
    if len(step.long_point) == 0:
        return step.start_tick

    return step.start_tick + step.long_point[-1].tick
    

#Because we need to be able to find tags by their attributes, there is not always a guarantee that the python abstraction of a tag passed in by the API will be a reference to the same tag in the ElementTree structure. so for those occasions where we need a guaranteed reference, use this
#tl;dr: If the passed 'objectToGet' matches an object in the collection using the equality operator, returns the object as found in the collection
def getReferenceByValue(parentTag: IXMLCollection, objectToGet):
    for item in parentTag:
        if item == objectToGet:
            return item

    return None

class Chart:
    #Either pass a chart root tag as xml.etree.ElementTree.Element, or pass nothing and create an empty chart
    def __init__(self, xml:xml.etree.ElementTree.Element = None, timeUnit = Ticks(480), endTick = Ticks(0)):
        if xml is not None:
            self.xml = chartRootXML(xml)
        else:
            self.xml = chartRootXML(createEmptyChartXML())
            self.xml.info.time_unit = timeUnit
            self.xml.info.end_tick = endTick

    @property
    def timeUnit(self):
        return self.xml.info.time_unit
    @timeUnit.setter
    def timeUnit(self, value):
        self.xml.info.time_unit = value

    @property
    def steps(self):
        return self.xml.sequence_data

    def addBPM(self, bpm: BPM, time: Ticks) -> Result:
        if bpm.bpm < 0:
            return Result.BPM_OUT_OF_BOUNDS 

        if bpm in self.xml.info.bpm_info:
            return Result.TICK_CONFLICT

        newBPM = bpmXML(createEmptyBPMXML())
        newBPM.tick = time
        newBPM.bpm = bpm.getBPMFormatted()

        newMeasure = measureXML(createEmptyMeasureXML())
        newMeasure.tick = time
        newMeasure.num = bpm.timeSigNum
        newMeasure.denomi = bpm.timeSigDenomi

        self.xml.info.bpm_info.append(newBPM)
        self.xml.info.measure_info.append(newMeasure)

        return Result.SUCCESS

    def addBPM_Raw(self, bpm: int, time: Ticks):
        if bpm < 0:
            return Result.BPM_OUT_OF_BOUNDS

        newBPM = bpmXML(createEmptyBPMXML())
        newBPM.tick = time
        newBPM.bpm = bpm

        self.xml.info.bpm_info.append(newBPM)
        return Result.SUCCESS

    def addMeasure(self, time: Ticks, num: int, denomi: int):
        if time < 0 or num < 1 or denomi < 1:
            return Result.MEASURE_OUT_OF_BOUNDS

        newMeasure = measureXML(createEmptyMeasureXML())
        newMeasure.tick = time
        newMeasure.num = num 
        newMeasure.denomi = denomi 

        self.xml.info.measure_info.append(newMeasure)
        
        return Result.SUCCESS

    def addMeasureRaw(self, measure: measureXML):
        if measure.tick < 0 or measure.num < 1 or measure.denomi < 1:
            return Result.MEASURE_OUT_OF_BOUNDS

        self.xml.info.measure_info.append(measure)

        return Result.SUCCESS

    def removeBPM(self, bpmTag: bpmXML):
        return self.xml.info.bpm_info.remove(bpmTag)        

    def removeMeasure(self, measureTag: measureXML):
        return self.xml.info.measure_info.remove(measureTag)

    def addNote(self, position: noteCoordinates, time: Ticks, playerID: PlayerID, stepType: StepTypes):
        if time < 0:
            return Result.TIME_OUT_OF_BOUNDS
        
        if position.left_pos < noteCoordinates.MIN or position.right_pos > noteCoordinates.MAX:
            return Result.NOTE_OUT_OF_BOUNDS

        newStep = stepXML(createEmptyStepXML())
        newStep.start_tick = time
        newStep.end_tick = time
        newStep.left_pos = position.left_pos
        newStep.right_pos = position.right_pos
        newStep.kind = stepType.value 
        newStep.player_id = playerID.value

        self.xml.sequence_data.append(newStep)

        return newStep

    def addNoteRaw(self, newNote: stepXML): 
        if newNote.start_tick < 0 or newNote.end_tick < 0 or newNote.end_tick < newNote.start_tick:
            return Result.TIME_OUT_OF_BOUNDS

        if newNote.left_pos < noteCoordinates.MIN or newNote.right_pos > noteCoordinates.MAX:
            return Result.NOTE_OUT_OF_BOUNDS

        if newNote.kind not in StepTypes:
            return Result.INVALID_STEP

        if newNote.player_id not in PlayerID:
            return Result.INVALID_PLAYER_ID
        
        self.xml.sequence_data.append(newNote)

        return Result.SUCCESS

    def removeNote(self, noteTag: stepXML):
        noteRef = getReferenceByValue(self.steps, noteTag)
        if noteRef is None:
            return Result.NOTE_DOESNT_EXIST
        return self.xml.sequence_data.remove(noteTag);

    def addLongPoint(self, stepToModify: stepXML, duration: Ticks):
        newPoint = pointXML(createEmptyPointXML())

        newPoint.tick = getLastTimeInStep(stepToModify) + duration
        newPoint.left_pos = stepToModify.left_pos
        newPoint.right_pos = stepToModify.right_pos

        stepToModify.end_tick = newPoint.tick
        
        returnVal = stepToModify.long_point.append(newPoint)
        
        return returnVal

    def addLongPointRaw(self, stepToModify: stepXML, newPoint: pointXML):
        stepRef = getReferenceByValue(self.steps, stepToModify)
        if stepRef is None:
            return Result.NOTE_DOESNT_EXIST

        if newPoint.left_pos > newPoint.right_pos or len([x for x in [newPoint.left_pos, newPoint.right_pos] if x < noteCoordinates.MIN or x > noteCoordinates.MAX]) != 0:
            return Result.NOTE_OUT_OF_BOUNDS

        if newPoint.left_end_pos is not None and newPoint.right_end_pos is not None:
            if len([x for x in [newPoint.left_end_pos, newPoint.right_end_pos] if x < noteCoordinates.MIN or x > noteCoordinates.MAX]) > 0:
                return Result.NOTE_OUT_OF_BOUNDS

        if newPoint.tick < getLastTimeInStep(stepRef):
            return Result.TIME_OUT_OF_BOUNDS

        stepRef.long_point.append(newPoint)
        stepRef.end_tick = newPoint.tick

        return Result.SUCCESS

    def removeLongPoint(self, stepToModify: stepXML, pointTag: longPointXML):
        stepRef = getReferenceByValue(self.steps, stepToModify)
        if stepRef is None:
            return Result.NOTE_DOESNT_EXIST

        if pointTag not in stepRef.long_point:
            return Result.NO_ACTION

        stepRef.long_point.remove(pointTag)

        return Result.SUCCESS

    def movePoint(self, stepToModify: stepXML, pointToModify: pointXML, position: noteCoordinates):
        if pointToModify not in stepToModify.long_point:
            return Result.INVALID_LONG_POINT

        pointToModify.left_pos = position.left_pos
        pointToModify.right_pos = position.right_pos

    def addSwipe(self, stepToModify: stepXML, pointToModify: pointXML, position: noteCoordinates):
        if pointToModify not in stepToModify.long_point:
            return Result.INVALID_LONG_POINT
        
        appendEndPosXML(pointToModify.innerElement)

        pointToModify.left_end_pos = position.left_pos
        pointToModify.right_end_pos = position.right_pos

    def addJump(self, time: Ticks):
        if time < 0:
            return Result.TIME_OUT_OF_BOUNDS

        newJump = stepXML(createEmptyStepXML())

        newJump.start_tick = time
        newJump.end_tick = time
        newJump.left_pos = noteCoordinates.MIN 
        newJump.right_pos = noteCoordinates.MAX 
        newJump.kind = StepTypes.JUMP.value 
        newJump.player_id = PlayerID.JUMPDOWN.value

        self.xml.sequence_data.append(newJump)

        return newJump
   
    def addDown(self, time: Ticks):
        if time < 0:
            return Result.TIME_OUT_OF_BOUNDS

        newDown = stepXML(createEmptyStepXML())

        newDown.start_tick = time
        newDown.end_tick = time
        newDown.left_pos = noteCoordinates.MIN 
        newDown.right_pos = noteCoordinates.MAX 
        newDown.kind = StepTypes.DOWN.value 
        newDown.player_id = PlayerID.JUMPDOWN.value

        self.xml.sequence_data.append(newDown)

        return newDown

    #It isn't currently clear what the param_id (named for the <id> tag inside <param>), lane, and 'tick' (for <extend><tick>) tags do, but these defaults appear to function fine 
    def addEffect(self, layerName: str, time: Ticks, speed: int, r = 0, g = 0, b = 0, extend_type = "Vfx", param_id = int(1), lane = int(0), tick = int(0)):
        if layerName not in layerNameValues.keys():
            return Result.INVALID_LAYER_NAME

        newEffect = extendTagXML(createEmptyExtendXML())
        newEffect.type_tag = extend_type
        newEffect.param.layer_name = layerName
        newEffect.param.time = time
        newEffect.param.kind = layerNameValues[newEffect.param.layer_name][0]
        newEffect.param.speed = speed

        #The <color> tag only exists for Background effects
        if layerNameValues[layerName][0] == "Background":
            if len([x for x in [r ,g, b] if x > -1 and x < 256]) != 3:
                return Result.COLOR_OUT_OF_RANGE
            
            appendColorTagXML(newEffect.param.innerElement)

            newEffect.param.color.red = r
            newEffect.param.color.green = g
            newEffect.param.color.blue = b

        newEffect.param.id = layerNameValues[layerName][2]
        newEffect.param.lane = lane
        newEffect.tick = time

        self.xml.extend_data.append(newEffect)

        return newEffect

    def save(self, filename: str) -> Result:
        self.xml.info.end_tick = 0
        for step in self.steps:
            if step.end_tick > self.xml.info.end_tick:
                self.xml.info.end_tick = step.end_tick

        return self.xml.write(filename)


#Get the literal coordinates of a note of size 'noteSize' at coordinate 'position' relative to 'relativeTo' (left or right)
#Returns None if the note would be out of bounds
def getPosition(noteSize: sizeUnit, position: int, relativeTo = 'L') -> noteCoordinates | Result:
    result = noteCoordinates()

    if relativeTo == 'L':
        result.left_pos = position
        result.right_pos = position + noteSize

        if result.right_pos > noteCoordinates.MAX or result.left_pos < noteCoordinates.MIN:
            return Result.NOTE_OUT_OF_BOUNDS
    elif relativeTo == 'R':
        result.left_pos = noteCoordiantes.MAX - position - noteSize
        result.right_pos = noteCoordinates.MAX - position

        if result.right_pos > noteCoordinates.MAX or result.left_pos < noteCoordinates.MIN:
            return Result.NOTE_OUT_OF_BOUNDS
    else:
        return Result.BAD_RELATIVE_POSITION 
        
    return result
