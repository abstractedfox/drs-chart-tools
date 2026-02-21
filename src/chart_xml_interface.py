import sys 
import xml.etree.ElementTree
from common import *

SEQ_VER = 9

#The usage pattern of this file is as such:
#Classes are for interfacing with XML structures that already exist in a pythonic way, they are really just an abstraction over the ElementTree module.
#To create new XML structures, use the functions that generate empty ones, then interface with them using the abstraction classes

#Generic functions implementing things for xml wrapper classes that we want to treat as collection types
class _IXMLCollection:
    def __init__(self):
        #in the subclass, set this to the abstracted type of the XML tag that this collection is supposed to track
        self.collection_type = None

        #in the subclass, set this to the actual ElementTree.Element object representing the tag
        self.inner_element = None

    def __getitem__(self, key):
        i = -1;
        last_element = None

        for item in self.inner_element:
            i += 1
            last_element = self.collection_type(item)

            if i == key:
                return self.collection_type(item)

        if (key < 0):
            return [self.collection_type(x) for x in self.inner_element][key];

        return None

    def __len__(self):
        i = 0
        for item in self.inner_element:
            i += 1

        return i

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        index_to_return = self.i
        self.i += 1

        if self.i > len(self):
            raise StopIteration

        return self[index_to_return]

    def __eq__(self, compare_to):
        if len(self) != len(compare_to):
            return False
        for item in self:
            if item not in compare_to:
                return False

        return True

    def append(self, newObject: collection_type):
        self.inner_element.append(newObject.inner_element)
        return self[-1]

    def remove(self, removeObject: collection_type):
        for item in self:
            if removeObject == item:
                self.inner_element.remove(item.inner_element)
                return Result.SUCCESS

        return Result.NO_ACTION

    def getElement(self, element):
        for item in self:
            if item == element:
                return item

        return None


#To be used on classes where we'd like to be able to use isinstance() to detect any of the tag implementations
class BaseXML:
    pass


class BpmXML(BaseXML):
    def __init__(self, bpmTag: xml.etree.ElementTree.Element):
        self.inner_element = bpmTag

    def __eq__(self, compare_to):
        return self.tick == compare_to.tick and self.bpm == compare_to.bpm

    @property
    def tick(self):
        return int(self.inner_element.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.inner_element.find("tick").text = str(value)

    @property
    def bpm(self):
        return int(self.inner_element.find("bpm").text)
    @bpm.setter
    def bpm(self, value):
        self.inner_element.find("bpm").text = str(value)


class MeasureXML(BaseXML):
    def __init__(self, measureTag: xml.etree.ElementTree.Element):
        self.inner_element = measureTag

    def __eq__(self, compare_to):
        return self.tick == compare_to.tick and self.num == compare_to.num and self.denomi == compare_to.denomi

    @property
    def tick(self):
        return int(self.inner_element.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.inner_element.find("tick").text = str(value)

    @property
    def num(self):
        return int(self.inner_element.find("num").text)
    @num.setter
    def num(self, value):
        self.inner_element.find("num").text = str(value)

    @property
    def denomi(self):
        return int(self.inner_element.find("denomi").text)
    @denomi.setter
    def denomi(self, value):
        self.inner_element.find("denomi").text = str(value)


#The <info> tag, ie the chart header
class ChartInfoXML(BaseXML):
    def __init__(self, chartRoot: xml.etree.ElementTree.Element):
        self.inner_element = chartRoot.find("info")

    @property
    def time_unit(self):
        return int(self.inner_element.find("time_unit").text)
    @time_unit.setter
    def time_unit(self, value):
        self.inner_element.find("time_unit").text = str(value)

    @property
    def end_tick(self):
        return int(self.inner_element.find("end_tick").text)
    @end_tick.setter
    def end_tick(self, value):
        self.inner_element.find("end_tick").text = str(value)

    @property
    def bpm_info(self):
        return BpmInfoXML(self.inner_element.find("bpm_info"))

    @property
    def measure_info(self):
        return MeasureInfoXML(self.inner_element.find("measure_info"))

#used inside <long_point>s
class PointXML(BaseXML):
    def __init__(self, pointTag: xml.etree.ElementTree.Element):
        self.inner_element = pointTag

    def __eq__(self, compare_to):
        return self.tick == compare_to.tick and self.left_pos == compare_to.left_pos and self.right_pos == compare_to.right_pos and not ((self.left_end_pos is None) ^ (self.left_end_pos is None)) and not ((self.right_end_pos is None) ^ (compare_to.right_end_pos is None)) and self.left_end_pos == compare_to.left_end_pos and self.right_end_pos == compare_to.right_end_pos 

    @property
    def tick(self):
        return int(self.inner_element.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.inner_element.find("tick").text = str(value)

    @property
    def left_pos(self):
        return int(self.inner_element.find("left_pos").text)
    @left_pos.setter
    def left_pos(self, value):
        self.inner_element.find("left_pos").text = str(value)

    @property
    def right_pos(self):
        return int(self.inner_element.find("right_pos").text)
    @right_pos.setter
    def right_pos(self, value):
        self.inner_element.find("right_pos").text = str(value)

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def left_end_pos(self):
        result = self.inner_element.find("left_end_pos")
        if result == None:
            return None
        return int(result.text)
    @left_end_pos.setter
    def left_end_pos(self, value):
        if self.inner_element.find("left_end_pos") is None:
            append_end_pos_XML(self.inner_element)
        self.inner_element.find("left_end_pos").text = str(value)

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def right_end_pos(self):
        result = self.inner_element.find("right_end_pos")
        if result is None:
            return None
        return int(result.text)
    @right_end_pos.setter
    def right_end_pos(self, value):
        if self.inner_element.find("right_end_pos") is None:
            append_end_pos_XML(self.inner_element)
        self.inner_element.find("right_end_pos").text = str(value)


class StepXML(BaseXML):
    def __init__(self, stepTag: xml.etree.ElementTree.Element):
        self.inner_element = stepTag

    def __eq__(self, compare_to):
        return self.start_tick == compare_to.start_tick and self.end_tick == compare_to.end_tick and self.left_pos == compare_to.left_pos and self.right_pos == compare_to.right_pos and self.kind == compare_to.kind and self.player_id == compare_to.player_id #and self.long_point == compare_to.long_point

    @property
    def start_tick(self):
        return int(self.inner_element.find("start_tick").text)
    @start_tick.setter
    def start_tick(self, value):
        self.inner_element.find("start_tick").text = str(value)

    @property
    def end_tick(self):
        return int(self.inner_element.find("end_tick").text)
    @end_tick.setter
    def end_tick(self, value):
        self.inner_element.find("end_tick").text = str(value)

    @property
    def left_pos(self):
        return int(self.inner_element.find("left_pos").text)
    @left_pos.setter
    def left_pos(self, value):
        self.inner_element.find("left_pos").text = str(value)

    @property
    def right_pos(self):
        return int(self.inner_element.find("right_pos").text)
    @right_pos.setter
    def right_pos(self, value):
        self.inner_element.find("right_pos").text = str(value)

    @property
    def kind(self):
        return int(self.inner_element.find("kind").text)
    @kind.setter
    def kind(self, value):
        self.inner_element.find("kind").text = str(value)

    @property
    def player_id(self):
        return int(self.inner_element.find("player_id").text)
    @player_id.setter
    def player_id(self, value):
        self.inner_element.find("player_id").text = str(value)

    @property
    def long_point(self):
        return LongPointXML(self.inner_element.find("long_point"))


class ColorTagXML:
    def __init__(self, colorTag: xml.etree.ElementTree.Element):
        self.inner_element = colorTag

    def __eq__(self, compare_to):
        return self.red == compare_to.red and self.green == compare_to.green and self.blue == compare_to.blue

    @property
    def red(self):
        return self.inner_element.find("red").text
    @red.setter
    def red(self, value):
        self.inner_element.find("red").text = str(value)

    @property
    def green(self):
        return self.inner_element.find("green").text
    @green.setter
    def green(self, value):
        self.inner_element.find("green").text = str(value)

    @property
    def blue(self):
        return self.inner_element.find("blue").text
    @blue.setter
    def blue(self, value):
        self.inner_element.find("blue").text = str(value)


class ParamTagXML:
    def __init__(self, paramTag: xml.etree.ElementTree.Element):
        self.inner_element = paramTag

    def __eq__(self, compare_to):
        return self.time == compare_to.time and self.kind == compare_to.kind and self.layer_name == compare_to.layer_name and self.id == compare_to.id and self.lane == compare_to.lane and self.speed == compare_to.speed and (~(self.color is None ^ compare_to.color is None) or (self.color is not None and compare_to.color is not None and self.color == compare_to.color))

    @property
    def time(self):
        return self.inner_element.find("time").text
    @time.setter
    def time(self, value):
        self.inner_element.find("time").text = str(value)

    @property
    def kind(self):
        return self.inner_element.find("kind").text
    @kind.setter
    def kind(self, value):
        self.inner_element.find("kind").text = str(value)

    @property
    def layer_name(self):
        return self.inner_element.find("layer_name").text
    @layer_name.setter
    def layer_name(self, value):
        self.inner_element.find("layer_name").text = str(value)

    @property
    def id(self):
        return self.inner_element.find("id").text
    @id.setter
    def id(self, value):
        self.inner_element.find("id").text = str(value)

    @property
    def lane(self):
        return self.inner_element.find("lane").text
    @lane.setter
    def lane(self, value):
        self.inner_element.find("lane").text = str(value)

    @property
    def speed(self):
        return self.inner_element.find("speed").text
    @speed.setter
    def speed(self, value):
        self.inner_element.find("speed").text = str(value)

    @property
    def color(self):
        return ColorTagXML(self.inner_element.find("color"))


class ExtendTagXML:
    def __init__(self, extendTag: xml.etree.ElementTree.Element):
        self.inner_element = extendTag

    def __eq__(self, compare_to):
        return self.type_tag == compare_to.type_tag and self.tick == compare_to.tick and self.param == compare_to.param
    
    @property
    def type_tag(self):
        return self.inner_element.find("type").text
    @type_tag.setter
    def type_tag(self, value):
        self.inner_element.find("type").text = str(value)

    @property
    def tick(self):
        return self.inner_element.find("tick").text
    @tick.setter
    def tick(self, value):
        self.inner_element.find("tick").text = str(value)

    @property
    def param(self):
        return ParamTagXML(self.inner_element.find("param"))


class MeasureInfoXML(_IXMLCollection):
    def __init__(self, MeasureInfoXMLRoot: xml.etree.ElementTree.Element):
        self.inner_element = MeasureInfoXMLRoot
        self.collection_type = MeasureXML

    def remove_at_index(self, index: int) -> Result:
        if index > (len(self) - 1):
            return Result.INVALID_INDEX

        try:
            self.inner_element.remove(self[index].inner_element)
        except Exception:
            return Result.MISC_ERROR

        return Result.SUCCESS


class BpmInfoXML(_IXMLCollection):
    def __init__(self, BpmInfoXMLRoot: xml.etree.ElementTree.Element):
        self.inner_element = BpmInfoXMLRoot
        self.collection_type = BpmXML

    def remove_at_index(self, index: int) -> Result:
        if index > (len(self) - 1):
            return Result.INVALID_INDEX

        try:
            self.inner_element.remove(self[index].inner_element)
        except Exception:
            return Result.MISC_ERROR

        return Result.SUCCESS


class LongPointXML(_IXMLCollection):
    def __init__(self, longPointTag: xml.etree.ElementTree.Element):
        self.inner_element = longPointTag
        self.collection_type = PointXML


class SequenceDataXML(_IXMLCollection):
    def __init__(self, sequenceDataTag: xml.etree.ElementTree.Element):
        self.inner_element = sequenceDataTag
        self.collection_type = StepXML


class ExtendDataTagXML(_IXMLCollection):
    def __init__(self, extendDataTag: xml.etree.ElementTree.Element):
        self.inner_element = extendDataTag
        self.collection_type = ExtendTagXML


#root tag of the chart
class ChartRootXML:
    def __init__(self, dataTag: xml.etree.ElementTree.Element):
        if not isinstance(dataTag, xml.etree.ElementTree.Element):
            raise TypeError("Can only instantiate with an ElementTree.Element")
        self.inner_element = dataTag

    @property
    def seq_version(self):
        return self.inner_element.find("seq_version").text
    @seq_version.setter
    def seq_version(self, value):
        self.inner_element.find("seq_version").text = str(value)

    @property
    def info(self):
        return ChartInfoXML(self.inner_element)

    @property
    def sequence_data(self):
        return SequenceDataXML(self.inner_element.find("sequence_data"))

    @property
    def extend_data(self):
        return ExtendDataTagXML(self.inner_element.find("extend_data"))

    def write(self, path) -> Result:
        assert isinstance(self.inner_element, xml.etree.ElementTree.Element)
        elementTree = xml.etree.ElementTree.ElementTree(element = self.inner_element)
        
        try:
            elementTree.write(path, 'UTF-8')
        except Exception as e:
            print("Exception raised while attempting to save file: ", e, file = sys.stderr)
            return Result.FILE_WRITE_ERROR
        
        return Result.SUCCESS


#Functions for initializing empty XML
def create_empty_BpmXML() -> xml.etree.ElementTree.Element:
    newBPM = xml.etree.ElementTree.Element("bpm")

    xml.etree.ElementTree.SubElement(newBPM, "tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newBPM, "bpm", {"__type": "s32"})

    return newBPM


def create_empty_MeasureXML() -> xml.etree.ElementTree.Element:
    newMeasure = xml.etree.ElementTree.Element("measure")

    xml.etree.ElementTree.SubElement(newMeasure, "tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newMeasure, "num", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newMeasure, "denomi", {"__type": "s32"})

    return newMeasure


def create_empty_ChartXML() -> xml.etree.ElementTree.Element:
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


def create_empty_StepXML() -> xml.etree.ElementTree.Element:
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
def create_empty_PointXML() -> xml.etree.ElementTree.Element:
    newPoint = xml.etree.ElementTree.Element("point")

    xml.etree.ElementTree.SubElement(newPoint, "tick", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newPoint, "left_pos", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(newPoint, "right_pos", {"__type": "s32"})
    
    return newPoint

#append *_end_pos tags to a <point> tag
def append_end_pos_XML(pointTag: xml.etree.ElementTree.Element):
    xml.etree.ElementTree.SubElement(pointTag, "left_end_pos", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(pointTag, "right_end_pos", {"__type": "s32"})

def append_ColorTagXML(paramTag: xml.etree.ElementTree.Element): 
    colorTag = xml.etree.ElementTree.SubElement(paramTag, "color")
    xml.etree.ElementTree.SubElement(colorTag, "red", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(colorTag, "green", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(colorTag, "blue", {"__type": "s32"})

    return colorTag

def create_empty_ExtendTagXML() -> xml.etree.ElementTree.Element:
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
