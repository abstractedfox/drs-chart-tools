import xml.etree.ElementTree
from common import *

SEQ_VER = 9

#The usage pattern of this file is as such:
#Classes are for interfacing with XML structures that already exist in a pythonic way, they are really just an abstraction over the ElementTree module.
#To create new XML structures, use the functions that generate empty ones, then interface with them using the abstraction classes

#Generic functions implementing things for xml wrapper classes that we want to treat as collection types
class IXMLCollection:
    #for each implementation of this class, set this to the abstracted type of the XML tag that this collection is supposed to track
    collectionType = None

    def __init__(self):
        pass

    def __getitem__(self, key):
        i = -1;
        lastElement = None

        for item in self.innerElement:
            i += 1
            lastElement = self.collectionType(item)

            if i == key:
                return self.collectionType(item)

        if (key == -1):
            #note to future generations: make this work properly and not just for -1 lol
            return lastElement

        return None

    def __len__(self):
        i = 0
        for item in self.innerElement:
            i += 1

        return i

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        indexToReturn = self.i
        self.i += 1

        if self.i > len(self):
            raise StopIteration

        return self[indexToReturn]

    def __eq__(self, compareTo):
        if len(self) != len(compareTo):
            return False
        for item in self:
            if item not in compareTo:
                return False

        return True

    def append(self, newObject: collectionType):
        self.innerElement.append(newObject.innerElement)
        return self[-1]

    def remove(self, removeObject: collectionType):
        for item in self:
            if removeObject == item:
                self.innerElement.remove(item.innerElement)
                return Result.SUCCESS

        return Result.NO_ACTION

    def getElement(self, element):
        for item in self:
            if item == element:
                return item

        return None


#To be used on classes where we'd like to be able to use isinstance() to detect any of the tag implementations
class baseXML:
    pass


class bpmXML(baseXML):
    def __init__(self, bpmTag: xml.etree.ElementTree.Element):
        self.innerElement = bpmTag

    def __eq__(self, compareTo):
        return self.tick == compareTo.tick and self.bpm == compareTo.bpm

    @property
    def tick(self):
        return int(self.innerElement.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.innerElement.find("tick").text = str(value)

    @property
    def bpm(self):
        return int(self.innerElement.find("bpm").text)
    @bpm.setter
    def bpm(self, value):
        self.innerElement.find("bpm").text = str(value)


class measureXML(baseXML):
    def __init__(self, measureTag: xml.etree.ElementTree.Element):
        self.innerElement = measureTag

    def __eq__(self, compareTo):
        return self.tick == compareTo.tick and self.num == compareTo.num and self.denomi == compareTo.denomi

    @property
    def tick(self):
        return int(self.innerElement.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.innerElement.find("tick").text = str(value)

    @property
    def num(self):
        return int(self.innerElement.find("num").text)
    @num.setter
    def num(self, value):
        self.innerElement.find("num").text = str(value)

    @property
    def denomi(self):
        return int(self.innerElement.find("denomi").text)
    @denomi.setter
    def denomi(self, value):
        self.innerElement.find("denomi").text = str(value)


#The <info> tag, ie the chart header
class chartInfo(baseXML):
    def __init__(self, chartRoot: xml.etree.ElementTree.Element):
        self.innerElement = chartRoot.find("info")

    @property
    def time_unit(self):
        return int(self.innerElement.find("time_unit").text)
    @time_unit.setter
    def time_unit(self, value):
        self.innerElement.find("time_unit").text = str(value)

    @property
    def end_tick(self):
        return int(self.innerElement.find("end_tick").text)
    @end_tick.setter
    def end_tick(self, value):
        self.innerElement.find("end_tick").text = str(value)

    @property
    def bpm_info(self):
        return bpmInfoXML(self.innerElement.find("bpm_info"))

    @property
    def measure_info(self):
        return measureInfoXML(self.innerElement.find("measure_info"))

#used inside <long_point>s
class pointXML(baseXML):
    def __init__(self, pointTag: xml.etree.ElementTree.Element):
        self.innerElement = pointTag

    def __eq__(self, compareTo):
        return self.tick == compareTo.tick and self.left_pos == compareTo.left_pos and self.right_pos == compareTo.right_pos and not ((self.left_end_pos is None) ^ (self.left_end_pos is None)) and not ((self.right_end_pos is None) ^ (compareTo.right_end_pos is None)) and self.left_end_pos == compareTo.left_end_pos and self.right_end_pos == compareTo.right_end_pos 

    @property
    def tick(self):
        return int(self.innerElement.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.innerElement.find("tick").text = str(value)

    @property
    def left_pos(self):
        return int(self.innerElement.find("left_pos").text)
    @left_pos.setter
    def left_pos(self, value):
        self.innerElement.find("left_pos").text = str(value)

    @property
    def right_pos(self):
        return int(self.innerElement.find("right_pos").text)
    @right_pos.setter
    def right_pos(self, value):
        self.innerElement.find("right_pos").text = str(value)

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def left_end_pos(self):
        result = self.innerElement.find("left_end_pos")
        if result == None:
            return None
        return int(result.text)
    @left_end_pos.setter
    def left_end_pos(self, value):
        if self.innerElement.find("left_end_pos") is None:
            appendEndPosXML(self.innerElement)
        self.innerElement.find("left_end_pos").text = str(value)

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def right_end_pos(self):
        result = self.innerElement.find("right_end_pos")
        if result is None:
            return None
        return int(result.text)
    @right_end_pos.setter
    def right_end_pos(self, value):
        if self.innerElement.find("right_end_pos") is None:
            appendEndPosXML(self.innerElement)
        self.innerElement.find("right_end_pos").text = str(value)


class stepXML(baseXML):
    def __init__(self, stepTag: xml.etree.ElementTree.Element):
        self.innerElement = stepTag

    def __eq__(self, compareTo):
        return self.start_tick == compareTo.start_tick and self.end_tick == compareTo.end_tick and self.left_pos == compareTo.left_pos and self.right_pos == compareTo.right_pos and self.kind == compareTo.kind and self.player_id == compareTo.player_id #and self.long_point == compareTo.long_point

    @property
    def start_tick(self):
        return int(self.innerElement.find("start_tick").text)
    @start_tick.setter
    def start_tick(self, value):
        self.innerElement.find("start_tick").text = str(value)

    @property
    def end_tick(self):
        return int(self.innerElement.find("end_tick").text)
    @end_tick.setter
    def end_tick(self, value):
        self.innerElement.find("end_tick").text = str(value)

    @property
    def left_pos(self):
        return int(self.innerElement.find("left_pos").text)
    @left_pos.setter
    def left_pos(self, value):
        self.innerElement.find("left_pos").text = str(value)

    @property
    def right_pos(self):
        return int(self.innerElement.find("right_pos").text)
    @right_pos.setter
    def right_pos(self, value):
        self.innerElement.find("right_pos").text = str(value)

    @property
    def kind(self):
        return int(self.innerElement.find("kind").text)
    @kind.setter
    def kind(self, value):
        self.innerElement.find("kind").text = str(value)

    @property
    def player_id(self):
        return int(self.innerElement.find("player_id").text)
    @player_id.setter
    def player_id(self, value):
        self.innerElement.find("player_id").text = str(value)

    @property
    def long_point(self):
        return longPointXML(self.innerElement.find("long_point"))


class colorTagXML:
    def __init__(self, colorTag: xml.etree.ElementTree.Element):
        self.innerElement = colorTag

    def __eq__(self, compareTo):
        return self.red == compareTo.red and self.green == compareTo.green and self.blue == compareTo.blue

    @property
    def red(self):
        return self.innerElement.find("red").text
    @red.setter
    def red(self, value):
        self.innerElement.find("red").text = str(value)

    @property
    def green(self):
        return self.innerElement.find("green").text
    @green.setter
    def green(self, value):
        self.innerElement.find("green").text = str(value)

    @property
    def blue(self):
        return self.innerElement.find("blue").text
    @blue.setter
    def blue(self, value):
        self.innerElement.find("blue").text = str(value)


class paramTagXML:
    def __init__(self, paramTag: xml.etree.ElementTree.Element):
        self.innerElement = paramTag

    def __eq__(self, compareTo):
        return self.time == compareTo.time and self.kind == compareTo.kind and self.layer_name == compareTo.layer_name and self.id == compareTo.id and self.lane == compareTo.lane and self.speed == compareTo.speed and (~(self.color is None ^ compareTo.color is None) or (self.color is not None and compareTo.color is not None and self.color == compareTo.color))

    @property
    def time(self):
        return self.innerElement.find("time").text
    @time.setter
    def time(self, value):
        self.innerElement.find("time").text = str(value)

    @property
    def kind(self):
        return self.innerElement.find("kind").text
    @kind.setter
    def kind(self, value):
        self.innerElement.find("kind").text = str(value)

    @property
    def layer_name(self):
        return self.innerElement.find("layer_name").text
    @layer_name.setter
    def layer_name(self, value):
        self.innerElement.find("layer_name").text = str(value)

    @property
    def id(self):
        return self.innerElement.find("id").text
    @id.setter
    def id(self, value):
        self.innerElement.find("id").text = str(value)

    @property
    def lane(self):
        return self.innerElement.find("lane").text
    @lane.setter
    def lane(self, value):
        self.innerElement.find("lane").text = str(value)

    @property
    def speed(self):
        return self.innerElement.find("speed").text
    @speed.setter
    def speed(self, value):
        self.innerElement.find("speed").text = str(value)

    @property
    def color(self):
        return colorTagXML(self.innerElement.find("color"))


class extendTagXML:
    def __init__(self, extendTag: xml.etree.ElementTree.Element):
        self.innerElement = extendTag

    def __eq__(self, compareTo):
        return self.type_tag == compareTo.type_tag and self.tick == compareTo.tick and self.param == compareTo.param
    
    @property
    def type_tag(self):
        return self.innerElement.find("type").text
    @type_tag.setter
    def type_tag(self, value):
        self.innerElement.find("type").text = str(value)

    @property
    def tick(self):
        return self.innerElement.find("tick").text
    @tick.setter
    def tick(self, value):
        self.innerElement.find("tick").text = str(value)

    @property
    def param(self):
        return paramTagXML(self.innerElement.find("param"))


class measureInfoXML(IXMLCollection):
    def __init__(self, measureInfoXMLRoot: xml.etree.ElementTree.Element):
        self.innerElement = measureInfoXMLRoot
        self.collectionType = measureXML

    def removeAtIndex(self, index: int) -> Result:
        if index > (len(self) - 1):
            return Result.INVALID_INDEX

        try:
            self.innerElement.remove(self[index].innerElement)
        except Exception:
            return Result.MISC_ERROR

        return Result.SUCCESS


class bpmInfoXML(IXMLCollection):
    def __init__(self, bpmInfoXMLRoot: xml.etree.ElementTree.Element):
        self.innerElement = bpmInfoXMLRoot
        self.collectionType = bpmXML

    def removeAtIndex(self, index: int) -> Result:
        if index > (len(self) - 1):
            return Result.INVALID_INDEX

        try:
            self.innerElement.remove(self[index].innerElement)
        except Exception:
            return Result.MISC_ERROR

        return Result.SUCCESS


class longPointXML(IXMLCollection):
    def __init__(self, longPointTag: xml.etree.ElementTree.Element):
        self.innerElement = longPointTag
        self.collectionType = pointXML


class sequenceDataXML(IXMLCollection):
    def __init__(self, sequenceDataTag: xml.etree.ElementTree.Element):
        self.innerElement = sequenceDataTag
        self.collectionType = stepXML


class extendDataTagXML(IXMLCollection):
    def __init__(self, extendDataTag: xml.etree.ElementTree.Element):
        self.innerElement = extendDataTag
        self.collectionType = extendTagXML


#root tag of the chart
class chartRootXML:
    def __init__(self, dataTag: xml.etree.ElementTree.Element):
        if not isinstance(dataTag, xml.etree.ElementTree.Element):
            raise TypeError("Can only instantiate with an ElementTree.Element")
        self.innerElement = dataTag

    @property
    def seq_version(self):
        return self.innerElement.find("seq_version").text
    @seq_version.setter
    def seq_version(self, value):
        self.innerElement.find("seq_version").text = str(value)

    @property
    def info(self):
        return chartInfo(self.innerElement)

    @property
    def sequence_data(self):
        return sequenceDataXML(self.innerElement.find("sequence_data"))

    @property
    def extend_data(self):
        return extendDataTagXML(self.innerElement.find("extend_data"))

    def write(self, path) -> Result:
        assert isinstance(self.innerElement, xml.etree.ElementTree.Element)
        elementTree = xml.etree.ElementTree.ElementTree(element = self.innerElement)
        
        try:
            elementTree.write(path, 'UTF-8')
        except:
            return Result.FILE_WRITE_ERROR
        
        return Result.SUCCESS


#Functions for initializing empty XML
def createEmptyBPMXML() -> xml.etree.ElementTree.Element:
    newBPM = xml.etree.ElementTree.Element("bpm")

    xml.etree.ElementTree.SubElement(newBPM, "tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newBPM, "bpm", {"__type": "s32"})

    return newBPM


def createEmptyMeasureXML() -> xml.etree.ElementTree.Element:
    newMeasure = xml.etree.ElementTree.Element("measure")

    xml.etree.ElementTree.SubElement(newMeasure, "tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newMeasure, "num", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newMeasure, "denomi", {"__type": "s32"})

    return newMeasure


def createEmptyChartXML() -> xml.etree.ElementTree.Element:
    newChart = xml.etree.ElementTree.Element("data")

    #We'll set this implicitly as we presently only handle sequence version 9
    seq_version = xml.etree.ElementTree.SubElement(newChart, "seq_version", {"__type": "s32"})
    seq_version.text = "9"

    infoTag = xml.etree.ElementTree.SubElement(newChart, "info")
    xml.etree.ElementTree.SubElement(infoTag, "time_unit", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(infoTag, "end_tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(infoTag, "bpm_info")
    xml.etree.ElementTree.SubElement(infoTag, "measure_info")

    sequenceDataTag = xml.etree.ElementTree.SubElement(newChart, "sequence_data")

    extendDataTag = xml.etree.ElementTree.SubElement(newChart, "extend_data")

    recDataTag = xml.etree.ElementTree.SubElement(newChart, "rec_data")

    return newChart


def createEmptyStepXML() -> xml.etree.ElementTree.Element:
    newStep = xml.etree.ElementTree.Element("step")

    xml.etree.ElementTree.SubElement(newStep, "start_tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newStep, "end_tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newStep, "left_pos", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newStep, "right_pos", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newStep, "kind", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newStep, "player_id", {"__type": "s32"})

    xml.etree.ElementTree.SubElement(newStep, "long_point")
    
    return newStep


#create an empty <point> tag (to be used in <step><long_point>)
def createEmptyPointXML() -> xml.etree.ElementTree.Element:
    newPoint = xml.etree.ElementTree.Element("point")

    xml.etree.ElementTree.SubElement(newPoint, "tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newPoint, "left_pos", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newPoint, "right_pos", {"__type": "s32"})
    
    return newPoint

#append *_end_pos tags to a <point> tag
def appendEndPosXML(pointTag: xml.etree.ElementTree.Element):
    xml.etree.ElementTree.SubElement(pointTag, "left_end_pos", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(pointTag, "right_end_pos", {"__type": "s32"})

def appendColorTagXML(paramTag: xml.etree.ElementTree.Element): 
    colorTag = xml.etree.ElementTree.SubElement(paramTag, "color")
    xml.etree.ElementTree.SubElement(colorTag, "red", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(colorTag, "green", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(colorTag, "blue", {"__type": "s32"})

    return colorTag

def createEmptyExtendXML() -> xml.etree.ElementTree.Element:
    newExtend = xml.etree.ElementTree.Element("extend")

    xml.etree.ElementTree.SubElement(newExtend, "type", {"__type": "str"})
    xml.etree.ElementTree.SubElement(newExtend, "tick", {"__type": "s32"})

    paramTag = xml.etree.ElementTree.SubElement(newExtend, "param")
    xml.etree.ElementTree.SubElement(paramTag, "time", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(paramTag, "kind", {"__type": "str"})
    xml.etree.ElementTree.SubElement(paramTag, "layer_name", {"__type": "str"})
    xml.etree.ElementTree.SubElement(paramTag, "id", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(paramTag, "lane", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(paramTag, "speed", {"__type": "s32"})

    #colorTag = xml.etree.ElementTree.SubElement(paramTag, "color")
    #xml.etree.ElementTree.SubElement(colorTag, "red", {"__type": "s32"})
    #xml.etree.ElementTree.SubElement(colorTag, "green", {"__type": "s32"})
    #xml.etree.ElementTree.SubElement(colorTag, "blue", {"__type": "s32"})

    return newExtend
