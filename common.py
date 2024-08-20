from enum import Enum

class Result(Enum):
    SUCCESS = 0
    NOTE_DOESNT_EXIST = 1
    NOTE_OUT_OF_BOUNDS = 2
    BPM_OUT_OF_BOUNDS = 3
    TIME_OUT_OF_BOUNDS = 4
    FILE_WRITE_ERROR = 5
    BAD_RELATIVE_POSITION = 6
    INVALID_INDEX = 7
    MISC_ERROR = 8
    LONG_POINT_ALRERADY_EXISTS = 9
    INVALID_LONG_POINT = 10
    INVALID_LAYER_NAME = 11
    COLOR_OUT_OF_RANGE = 12
    CHART_PARSING_ERROR = 13
    CHART_NOT_LOADED = 14
    NO_ACTION = 15
    TICK_CONFLICT = 16 #for trying to add elements that there can only be one of per tick, such as a bpm, when there is already one there
    BPM_DOESNT_EXIST = 17
