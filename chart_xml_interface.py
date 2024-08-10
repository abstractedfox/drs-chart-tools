import xml.etree.ElementTree

SEQ_VER = 9

#The usage pattern of this file is as such:
#Classes are for interfacing with XML structures that already exist in a pythonic way, they are really just an abstraction over the ElementTree module.
#To create new XML structures, use the functions that generate empty ones, then interface with them using the abstraction classes

class XMLbpm:
    def __init__(self, bpmTag: xml.etree.ElementTree.Element):
        self.bpmElement = bpmTag

    @property
    def tick(self):
        return int(self.bpmElement.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.bpmElement.find("tick").text = str(value)

    @property
    def bpm(self):
        return int(self.bpmElement.find("bpm").text)
    @bpm.setter
    def bpm(self, value):
        self.bpmElement.find("bpm").text = str(value)

#Since this tag does nothing but contain <bpm> tags, we're essentially just going to have it be a container class that you access with array indexing
class bpmInfo:
    def __init__(self, bpmInfoRoot: xml.etree.ElementTree.Element):
        self.bpmInfoElement = bpmInfoRoot

    def __getitem__(self, key):
        i = -1;

        for bpm in self.bpmInfoElement:
            i += 1
            if i == key:
                return XMLbpm(bpm)

        return None

    def append(self, newBPM: XMLbpm):
        self.bpmInfoElement.append(newBPM.bpmElement)

    def removeAtIndex(self, index: int):
        self.bpmInfoElement.remove(self[index])


class XMLmeasure:
    def __init__(self, measureTag: xml.etree.ElementTree.Element):
        self.measureElement = measureTag

    @property
    def tick(self):
        return int(self.measureElement.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.measureElement.find("tick").text = str(value)

    @property
    def num(self):
        return int(self.measureElement.find("num").text)
    @num.setter
    def num(self, value):
        self.measureElement.find("num").text = str(value)

    @property
    def denomi(self):
        return int(self.measureElement.find("denomi").text)
    @denomi.setter
    def denomi(self, value):
        self.measureElement.find("denomi").text = str(value)

class measureInfo:
    def __init__(self, measureInfoRoot: xml.etree.ElementTree.Element):
        self.measureInfoElement = measureInfoRoot

    def __getitem__(self, key):
        i = -1;

        for measure in self.measureInfoElement:
            i += 1
            if i == key:
                return XMLmeasure(measure)

        return None

    def append(self, newMeasure: XMLmeasure):
        self.measureInfoElement.append(newMeasure.measureElement)

#The <info> tag, ie the chart header
class chartInfo:
    def __init__(self, chartRoot: xml.etree.ElementTree.Element):
        self.infoTagElement = chartRoot.find("info")

    @property
    def time_unit(self):
        return int(self.infoTagElement.find("time_unit").text)
    @time_unit.setter
    def time_unit(self, value):
        self.infoTagElement.find("time_unit").text = str(value)

    @property
    def end_tick(self):
        return int(self.infoTagElement.find("end_tick").text)
    @end_tick.setter
    def end_tick(self, value):
        self.infoTagElement.find("end_tick").text = str(value)

    @property
    def bpm_info(self):
        return bpmInfo(self.infoTagElement.find("bpm_info"))

    @property
    def measure_info(self):
        return measureInfo(self.infoTagElement.find("measure_info"))

#used inside <long_point>s
class XMLpoint:
    def __init__(self, pointTag: xml.etree.ElementTree.Element):
        self.pointTagElement = pointTag

    @property
    def tick(self):
        return int(self.stepTagElement.find("tick").text)
    @tick.setter
    def tick(self, value):
        self.stepTagElement.find("tick").text = str(value)

    @property
    def start_tick(self):
        return int(self.stepTagElement.find("start_tick").text)
    @start_tick.setter
    def start_tick(self, value):
        self.stepTagElement.find("start_tick").text = str(value)

    @property
    def left_pos(self):
        return int(self.stepTagElement.find("left_pos").text)
    @left_pos.setter
    def left_pos(self, value):
        self.stepTagElement.find("left_pos").text = str(value)

    @property
    def right_pos(self):
        return int(self.stepTagElement.find("right_pos").text)
    @right_pos.setter
    def right_pos(self, value):
        self.stepTagElement.find("right_pos").text = str(value)

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def left_end_pos(self):
        return int(self.stepTagElement.find("left_end_pos").text)
    @left_end_pos.setter
    def left_end_pos(self, value):
        self.stepTagElement.find("left_end_pos").text = str(value)

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def right_end_pos(self):
        return int(self.stepTagElement.find("right_end_pos").text)
    @right_end_pos.setter
    def right_end_pos(self, value):
        self.stepTagElement.find("right_end_pos").text = str(value)


class XMLstep:
    def __init__(self, stepTag: xml.etree.ElementTree.Element):
        self.stepTagElement = stepTag

    @property
    def start_tick(self):
        return int(self.stepTagElement.find("start_tick").text)
    @start_tick.setter
    def start_tick(self, value):
        self.stepTagElement.find("start_tick").text = str(value)

    @property
    def end_tick(self):
        return int(self.stepTagElement.find("end_tick").text)
    @end_tick.setter
    def end_tick(self, value):
        self.stepTagElement.find("end_tick").text = str(value)

    @property
    def left_pos(self):
        return int(self.stepTagElement.find("left_pos").text)
    @left_pos.setter
    def left_pos(self, value):
        self.stepTagElement.find("left_pos").text = str(value)

    @property
    def right_pos(self):
        return int(self.stepTagElement.find("right_pos").text)
    @right_pos.setter
    def right_pos(self, value):
        self.stepTagElement.find("right_pos").text = str(value)

    @property
    def kind(self):
        return int(self.stepTagElement.find("kind").text)
    @kind.setter
    def kind(self, value):
        self.stepTagElement.find("kind").text = str(value)

    @property
    def player_id(self):
        return int(self.stepTagElement.find("player_id").text)
    @player_id.setter
    def player_id(self, value):
        self.stepTagElement.find("player_id").text = str(value)


class sequenceDataXML:
    def __init__(self, sequenceDataTag: xml.etree.ElementTree.Element):
        self.sequenceDataElement = sequenceDataTag

    def __getitem__(self, key):
        i = -1;

        for step in self.sequenceDataElement:
            i += 1
            if i == key:
                return XMLstep(step)

        return None

    def append(self, stepTag: XMLstep):
        self.sequenceDataElement.append(stepTag.stepTagElement)

class colorTagXML:
    def __init__(self, colorTag: xml.etree.ElementTree.Element):
        self.colorTag = colorTag

    @property
    def red(self):
        return self.colorTag.find("red").text
    @red.setter
    def red(self, value):
        self.colorTag.find("red").text = str(value)

    @property
    def green(self):
        return self.colorTag.find("green").text
    @green.setter
    def green(self, value):
        self.colorTag.find("green").text = str(value)

    @property
    def blue(self):
        return self.colorTag.find("blue").text
    @blue.setter
    def blue(self, value):
        self.colorTag.find("blue").text = str(value)


class paramTagXML:
    def __init__(self, paramTag: xml.etree.ElementTree.Element):
        self.paramTag = paramTag

    @property
    def time(self):
        return self.paramTag.find("time").text
    @time.setter
    def time(self, value):
        self.paramTag.find("time").text = str(value)

    @property
    def kind(self):
        return self.paramTag.find("kind").text
    @kind.setter
    def kind(self, value):
        self.paramTag.find("kind").text = str(value)

    @property
    def layer_name(self):
        return self.paramTag.find("layer_name").text
    @layer_name.setter
    def layer_name(self, value):
        self.paramTag.find("layer_name").text = str(value)

    @property
    def id(self):
        return self.paramTag.find("id").text
    @id.setter
    def id(self, value):
        self.paramTag.find("id").text = str(value)

    @property
    def lane(self):
        return self.paramTag.find("lane").text
    @lane.setter
    def lane(self, value):
        self.paramTag.find("lane").text = str(value)
        
    @property
    def speed(self):
        return self.paramTag.find("speed").text
    @speed.setter
    def speed(self, value):
        self.paramTag.find("speed").text = str(value)

    @property
    def color(self):
        return colorTagXML(self.paramTag.find("color")) 

class extendTagXML:
    def __init__(self, extendTag: xml.etree.ElementTree.Element):
        self.extendTag = extendTag

    @property
    def type(self):
        return self.extendTag.find("type").text
    @type.setter
    def type(self, value):
        self.extendTag.find("type").text = str(value)

    @property
    def tick(self):
        return self.extendTag.find("tick").text
    @tick.setter
    def tick(self, value):
        self.extendTag.find("tick").text = str(value)
    
    @property
    def param(self):
        return paramTagXML(self.extendTag.find("param"))


class extendDataTagXML:
    def __init__(self, extendDataTag: xml.etree.ElementTree.Element):
        self.extendDataTag = extendDataTag

    def __getitem__(self, key):
        i = -1;

        for extendTag in self.extendDataTag:
            i += 1
            if i == key:
                return extendTag

        return None

#root tag of the chart
class chartRootXML:
    def __init__(self, dataTag: xml.etree.ElementTree.Element):
        self.dataTag = dataTag

    @property
    def seq_version(self):
        return self.dataTag.find("seq_version").text
    @seq_version.setter
    def seq_version(self, value):
        self.dataTag.find("seq_version").text = str(value)

    @property
    def info(self):
        return chartInfo(self.dataTag)

    @property
    def sequence_data(self):
        return sequenceDataXML(self.dataTag.find("sequence_data"))

    @property
    def extend_data(self):
        return extendDataTagXML(self.dataTag.find("extend_data"))

    def write(self, path):
        elementTree = xml.etree.ElementTree.ElementTree(element = self.dataTag)
        elementTree.write(path, 'UTF-8')


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
    
