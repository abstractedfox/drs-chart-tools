from enum import Enum

class Result(Enum):
    SUCCESS = 0
    NOTE_DOESNT_EXIST = 1
    NOTE_OUT_OF_BOUNDS = 2
    BPM_OUT_OF_BOUNDS = 3
    TIME_OUT_OF_BOUNDS = 4
    FILE_WRITE_ERROR = 5
    BAD_RELATIVE_POSITION = 6
