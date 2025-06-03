from dataclasses import dataclass

from chart_xml_interface import *
from common import *


def add_dict_commons(dictionary):
    dictionary["exists"] = 1 #by default, the tag exists

#Dict structures to be used by the API, use these to ensure correctness
def new_bpm_info_dict(tick: 0, bpm: 0):
    return add_dict_commons({"tick": tick, "bpm": bpm})

def new_measure_info_dict(tick = 0, num = 0, denomi = 0):
    return add_dict_commons({"tick": tick, "num": num, "denomi": denomi})

def new_step_dict(start_tick = 0, end_tick = 0, left_pos = 0, right_pos = 0, kind = 1, player_id = 0):
    return add_dict_commons({"start_tick": start_tick, "end_tick": end_tick, "left_pos": left_pos, "right_pos": right_pos, "kind": kind, "player_id": player_id})

def new_point_dict(tick = 0, left_pos = 0, right_pos = 0, left_end_pos = 0, right_end_pos = 0):
    return add_dict_commons({"tick": tick, "left_pos": left_pos, "right_pos": right_pos, "left_end_pos": left_end_pos, "right_end_pos": right_end_pos})

class verifydict:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __setitem__(self, key, value):
        if key not in self.dictionary:
            raise KeyError
        
        self.dictionary["key"] = value
