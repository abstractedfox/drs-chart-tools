import xml.etree.ElementTree

SEQ_VER = 9

#for what i think is simplicity reasons, we will deal with everything as xml structures (via ElementTree) since that is how everything starts and ends


class XMLbpm:
    def __init__(self, bpmTag: xml.etree.ElementTree.Element):
        self.bpmElement = bpmTag

    @property
    def tick(self):
        return self.bpmElement.find("tick").text
    @tick.setter
    def tick(self, value):
        self.bpmElement.find("tick").text = value

    @property
    def bpm(self):
        return self.bpmElement.find("bpm").text
    @bpm.setter
    def bpm(self, value):
        self.bpmElement.find("bpm").text = value

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

    def append(newBPM: XMLbpm):
        self.bpmInfoElement.append(XMLbpm)

    def removeAtIndex(index: int):
        self.bpmInfoElement.remove(self[index])


class XMLmeasure:
    def __init__(self, measureTag: xml.etree.ElementTree.Element):
        self.measureElement = measureTag

    @property
    def tick(self):
        return self.measureElement.find("tick").text
    @tick.setter
    def tick(self, value):
        self.measureElement.find("tick").text = value

    @property
    def num(self):
        return self.measureElement.find("num").text
    @num.setter
    def num(self, value):
        self.measureElement.find("num").text = value

    @property
    def denomi(self):
        return self.measureElement.find("denomi").text
    @denomi.setter
    def denomi(self, value):
        self.measureElement.find("denomi").text = value

class measureInfo:
    def __init__(self, measureInfoRoot: xml.etree.ElementTree.Element):
        self.measureInfoElement = measureInfoRoot

    def __getitem__(self, key):
        i = -1;

        for measure in self.measureInfoElement:
            i += 1
            if i == key:
                return XMLmeasure(measure)

#The <info> tag, ie the chart header
class chartInfo:
    def __init__(self, chartRoot: xml.etree.ElementTree.Element):
        self.infoTagElement = chartRoot.find("info")

    @property
    def time_unit(self):
        return self.infoTagElement.find("time_unit").text
    @time_unit.setter
    def time_unit(self, value):
        self.infoTagElement.find("time_unit").text = value

    @property
    def end_tick(self):
        return self.infoTagElement.find("end_tick").text
    @end_tick.setter
    def end_tick(self, value):
        self.infoTagElement.find("end_tick").text = value

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
        return self.stepTagElement.find("tick").text
    @tick.setter
    def tick(self, value):
        self.stepTagElement.find("tick").text = value

    @property
    def start_tick(self):
        return self.stepTagElement.find("start_tick").text
    @start_tick.setter
    def start_tick(self, value):
        self.stepTagElement.find("start_tick").text = value

    @property
    def left_pos(self):
        return self.stepTagElement.find("left_pos").text
    @left_pos.setter
    def left_pos(self, value):
        self.stepTagElement.find("left_pos").text = value

    @property
    def right_pos(self):
        return self.stepTagElement.find("right_pos").text
    @right_pos.setter
    def right_pos(self, value):
        self.stepTagElement.find("right_pos").text = value

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def left_end_pos(self):
        return self.stepTagElement.find("left_end_pos").text
    @left_end_pos.setter
    def left_end_pos(self, value):
        self.stepTagElement.find("left_end_pos").text = value

    #This tag does not always exist, so this can return None under normal conditions
    @property
    def right_end_pos(self):
        return self.stepTagElement.find("right_end_pos").text
    @right_end_pos.setter
    def right_end_pos(self, value):
        self.stepTagElement.find("right_end_pos").text = value


class XMLstep:
    def __init__(self, stepTag: xml.etree.ElementTree.Element):
        self.stepTagElement = stepTag

    @property
    def start_tick(self):
        return self.stepTagElement.find("start_tick").text
    @start_tick.setter
    def start_tick(self, value):
        self.stepTagElement.find("start_tick").text = value

    @property
    def end_tick(self):
        return self.stepTagElement.find("end_tick").text
    @end_tick.setter
    def end_tick(self, value):
        self.stepTagElement.find("end_tick").text = value

    @property
    def left_pos(self):
        return self.stepTagElement.find("left_pos").text
    @left_pos.setter
    def left_pos(self, value):
        self.stepTagElement.find("left_pos").text = value

    @property
    def right_pos(self):
        return self.stepTagElement.find("right_pos").text
    @right_pos.setter
    def right_pos(self, value):
        self.stepTagElement.find("right_pos").text = value

    @property
    def kind(self):
        return self.stepTagElement.find("kind").text
    @kind.setter
    def kind(self, value):
        self.stepTagElement.find("kind").text = value

    @property
    def player_id(self):
        return self.stepTagElement.find("player_id").text
    @player_id.setter
    def player_id(self, value):
        self.stepTagElement.find("player_id").text = value

class sequence_data:
    def __init__(self, sequenceDataTag: xml.etree.ElementTree.Element):
        self.sequenceDataElement = sequenceDataTag

    def __getitem__(self, key):
        i = -1;

        for step in self.sequenceDataElement:
            i += 1
            if i == key:
                return XMLstep(step)
