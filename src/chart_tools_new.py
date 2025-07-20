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


def new_step_dict(start_tick = 0, end_tick = 0, left_pos = 0, right_pos = 0, kind = 1, player_id = 0, long_point = None):
    long_point_val = [] if long_point is None else long_point
    result = {"type": "step", "start_tick": start_tick, "end_tick": end_tick, "left_pos": left_pos, "right_pos": right_pos, "kind": kind, "player_id": player_id, "long_point": long_point_val}
    add_dict_commons(result)
    return result


def new_point_dict(tick = 0, left_pos = 0, right_pos = 0, left_end_pos = None, right_end_pos = None):
    result = {"type": "point", "tick": tick, "left_pos": left_pos, "right_pos": right_pos, "left_end_pos": left_end_pos, "right_end_pos": right_end_pos}
    add_dict_commons(result)
    return result


def new_extend_dict(type_tag = "Vfx", tick = 0, time = 0, kind = "", layer_name = "", id_tag = 0, lane = 0, speed = 0, r = 0, g = 0, b = 0):
    result = {"type": type_tag, "tick": tick, "time": time, "kind": kind, "layer_name": layer_name, "id": id_tag, "lane": lane, "speed": speed, "r": r, "g": g, "b": b}
    add_dict_commons(result)
    return result


#Prevent accidentally adding a key to a dict 
class verifydict:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __setitem__(self, key, value):
        if key not in self.dictionary:
            raise KeyError(key)
        
        self.dictionary[key] = value


#For a given chart element represented as a dict, receive it as an appropriate wrapper class instance from chart_xml_interface
def object_from_dict(dictionary):
    result = None
    
    if type(dictionary) != dict:
        raise TypeError("Needed dict, not {}".format(dictionary))

    match dictionary["type"]:
        case "bpm_info":
            result = bpmXML(createEmptyBPMXML())

        case "measure_info":
            result = measureXML(createEmptyMeasureXML())
        
        case "step":
            result = stepXML(createEmptyStepXML())

        case "point":
            result = pointXML(createEmptyPointXML())

    if dictionary["type"] == "point" and dictionary["left_end_pos"] == None and dictionary["right_end_pos"] == None:
        dictionary.pop("left_end_pos")
        dictionary.pop("right_end_pos")

    for key in dictionary:
        if key == "long_point":
            if len(dictionary["long_point"]) > 0:
                for point in dictionary["long_point"]:
                   result.long_point.append(object_from_dict(point))
            else:
                continue
        elif key in dir(result):
            setattr(result, key, dictionary[key])
        elif key != "type" and key != "exists":
            raise KeyError(key)
    
    return result


#For a given chart element represented as a wrapper class instance, receive it as an appropriate dict
def dict_from_object(classinstance):
    class dummy:
        def __init__(self):
            pass

    result = None
    if type(classinstance) == bpmXML:
        result = new_bpm_info_dict()

    if type(classinstance) ==  measureXML:
        result = new_measure_info_dict()

    if type(classinstance) == stepXML:
        result = new_step_dict()

    if type(classinstance) == pointXML:
        result = new_point_dict()

    for key in [x for x in dir(classinstance) if x not in dir(dummy())]:
        if key == "innerElement":
            continue
        if key == "long_point":
            for point in getattr(classinstance, "long_point"):
                result["long_point"].append(dict_from_object(point))
        else:
            verifydict(result)[key] = getattr(classinstance, key)

    return result


def new_chart() -> chartRootXML:
    return chartRootXML(createEmptyChartXML())


#Where 'element' is a bpm, measure, step, or point.
#Element is added to the chart by default or removed from the chart (if it exists) if remove == True
def update_chart(chart: chartRootXML, element, remove = False, point_parent_step = None, return_elements = False) -> Optional[Union[Result|baseXML]]:
    if type(element) == stepXML:
        if remove:
            return chart.sequence_data.remove(element)
        
        exists = chart.sequence_data.getElement(element)

        if exists is not None:
            return Result.NOTE_ALREADY_EXISTS
        
        new_end_tick = element.start_tick #the only time start_tick isn't identical to end_tick is when there are long_points
        
        for point in element.long_point:
            update_chart(chart, point, point_parent_step = element)
            new_end_tick = point.tick

        #note: this append was moved from before the loop so we could calculate end_tick after long points. if there is any apparent weirdness surrounding this in the future, suspect this change
        element.end_tick = new_end_tick
        chart.sequence_data.append(element)
        return element if return_elements else Result.SUCCESS

    if type(element) == measureXML:
        if remove:
            return chart.info.measure_info.remove(element)

        exists = chart.info.measure_info.getElement(element)

        if exists is not None:
            return Result.MEASURE_ALREADY_EXISTS
        
        chart.info.measure_info.append(element)
        return element if return_elements else Result.SUCCESS
    
    if type(element) == bpmXML:
        if remove:
            return chart.info.bpm_info.remove(element)

        exists = chart.info.bpm_info.getElement(element)

        if exists is not None:
            return Result.BPM_ALREADY_EXISTS
        
        chart.info.bpm_info.append(element)
        return element if return_elements else Result.SUCCESS

    if type(element) == pointXML: 
        if point_parent_step is None:
            return Result.INVALID_LONG_POINT
        
        if point_parent_step not in chart.sequence_data:
            return Result.NOTE_DOESNT_EXIST

        if remove:
            return chart.sequence_data.getElement(point_parent_step).long_point.remove(element)

        exists = chart.sequence_data.getElement(point_parent_step).long_point.getElement(element)

        if exists is not None:
            return Result.POINT_ALREADY_EXISTS

        step_in_chart = chart.sequence_data.getElement(point_parent_step)
        step_in_chart.long_point.append(element)
        
        #Ensure long_points are sorted by tick ascending
        #This drastically simplifies rendering them in the frontend, but is also how it's done in reference charts
        for i in range(1, len(step_in_chart.long_point)):
            while step_in_chart.long_point[i] < step_in_chart.long_point[i-1]:
                temp = step_in_chart.long_point[i-1]
                step_in_chart.long_point[i-1] = step_in_chart.long_point[i]
                step_in_chart.long_point[i] = temp 

        return element if return_elements else Result.SUCCESS


def update_chart_diff(chart: chartRootXML, element, remove = False, point_parent_step = None, diff = [], diff_as_dicts = True) -> Result:
    result = update_chart(chart, element, remove = remove, point_parent_step = point_parent_step, return_elements = True)
    
    #When the return_elements arg is True, update_chart returns the actual element that was added to indicate success
    if isinstance(result, baseXML):
        element = result
        result = Result.SUCCESS

    if result == Result.SUCCESS:
        if diff_as_dicts: 
            diff.append(dict_from_object(element))
            diff[-1]["exists"] = not remove
        else:
            diff.append({element, remove})
    
    return result


def save_chart(chart: chartRootXML, filename: str) -> Result:
    chart.info.end_tick = 0
    for step in chart.sequence_data:
        if step.end_tick > chart.info.end_tick:
            chart.info.end_tick = step.end_tick

    return chart.write(filename)
