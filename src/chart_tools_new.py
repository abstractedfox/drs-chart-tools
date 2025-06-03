from chart_xml_interface import *
from common import *


def add_dict_commons(dictionary):
    dictionary["exists"] = 1 #by default, the tag exists (using int for interop w js)


#Dict structures to be used by the API, use these to ensure correctness
def new_bpm_info_dict(tick = 0, bpm = 0):
    result = {"type": "bpm_info", "tick": tick, "bpm": bpm}
    add_dict_commons(result)
    return result

def new_measure_info_dict(tick = 0, num = 0, denomi = 0):
    result = {"type": "measure_info", "tick": tick, "num": num, "denomi": denomi}
    add_dict_commons(result)
    return result

def new_step_dict(start_tick = 0, end_tick = 0, left_pos = 0, right_pos = 0, kind = 1, player_id = 0):
    result = {"type": "step", "start_tick": start_tick, "end_tick": end_tick, "left_pos": left_pos, "right_pos": right_pos, "kind": kind, "player_id": player_id}
    add_dict_commons(result)
    return result

def new_point_dict(tick = 0, left_pos = 0, right_pos = 0, left_end_pos = 0, right_end_pos = 0):
    result = {"type": "point", "tick": tick, "left_pos": left_pos, "right_pos": right_pos, "left_end_pos": left_end_pos, "right_end_pos": right_end_pos}
    add_dict_commons(result)
    return result


#Prevent accidentally adding a key to a dict 
class verifydict:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __setitem__(self, key, value):
        if key not in self.dictionary:
            raise KeyError(key)
        
        self.dictionary["key"] = value


#For a given chart element represented as a dict, receive it as an appropriate wrapper class instance from chart_xml_interface
def object_from_dict(dictionary):
    result = None
    match dictionary["type"]:
        case "bpm_info":
            result = bpmXML(createEmptyBPMXML())

        case "measure_info":
            result = measureXML(createEmptyMeasureXML())
        
        case "step":
            result = stepXML(createEmptyStepXML())

        case "point":
            result = pointXML(createEmptyPointXML())

    for key in dictionary:
        if key in dir(result):
            setattr(result, key, dictionary[key])
        elif key != "type" and key != "exists":
            raise KeyError(key)
    
    return result


#Where 'element' is a bpm, measure, step, or point.
#Element is added to the chart by default or removed from the chart (if it exists) if remove == True
#This is currently untested!
def update_chart(chart: chartXML, element, remove = False) -> Result:
    if type(element) == stepXML:
        if remove:
            return chart.sequence_data.remove(element)
        
        exists = chart.sequence_data.getElement(element)

        if exists is not None:
            return Result.NOTE_ALREADY_EXISTS
        chart.sequence_data.append(element)
