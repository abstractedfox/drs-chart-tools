from dataclasses import dataclass

from chart_xml_interface import *
from common import *


def add_dict_commons(dictionary):
    dictionary["exists"] = 1 #by default, the tag exists
    

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

#Prevent modifying a key in a dictionary if it doesn't already exist
class verifydict:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __setitem__(self, key, value):
        if key not in self.dictionary:
            raise KeyError
        
        self.dictionary["key"] = value

#For a given chart element represented as a dict, receive it as an appropriate wrapper type from chart_xml_interface
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
        setattr(result, key, dictionary[key])

    return result
