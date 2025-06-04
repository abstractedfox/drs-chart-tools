from runtime import *

from flask import Flask, jsonify, request

app = Flask(__name__)

_session = None

apiresults = {
    "UNDEFINED": "UNDEFINED",
    "BAD_REQUEST": "BAD_REQUEST",
    "BAD_DATA": "BAD_DATA",
    "NOT_INITIALIZED": "NOT_INITIALIZED",
    "SUCCESS": "SUCCESS",
    "TRUE": "TRUE",
    "FALSE": "FALSE",
    "INVALID_FUNCTION": "INVALID_FUNCTION",
    "FAILED": "FAILED"
}

def new_response(result = apiresults["UNDEFINED"], error_info = None, diff = [], steps = [], bpms = [], measures = []):
    response = {"head": {"result": result}, "data": {}}
    if result not in apiresults:
        raise NameError("\"{}\" not found in apiresults.".format(result))

    if error_info:
        response["data"]["error_info"] = error_info

    if steps:
        if type(steps) != type([]):
            raise TypeError("steps must be a list")
        response["data"]["steps"] = steps

    if bpms:
        if type(bpms) != type([]):
            raise TypeError("bpms must be a list")
        response["data"]["bpms"] = bpms
    
    if measures:
        if type(measures) != type([]):
            raise TypeError("measures must be a list")
        response["data"]["measures"] = measures
    
    if diff:
        if type(diff) != type([]):
            raise TypeError("Diff must be a list")
        response["data"]["diff"] = diff

    #where head["result"] is the result of an operation (if relevant) and data is any data (if relevant)
    return response 

#Request reference, also useful for testing
def new_request(function = "", data = {}, changes = []):
    request = {"head": {"function": function}, "data": data}

    match function:
        case "update_chart":
            data["changes"] = changes

    return request

@app.route("/api", methods=["POST"])
def api():
    global _session
    
    log("Received request: {}".format(request.json))
    if "head" not in request.json:
        response = new_response()
        verifydict(response["head"])["result"] = apiresults["BAD_REQUEST"] 
        return response
   
    head = request.json["head"]
    data = request.json["data"]
    match head["function"]:
        case "init":
            _session = Session(path = data["filename"]) 
            return new_response(result = apiresults["SUCCESS"])

        case "save":
            result = _session.save() 

            if result == Result.SUCCESS:
                return new_response(result = apiresults["SUCCESS"])
            else:
                return new_response(result = apiresults["FAILED"], error_info = result.name)

        case "close_session":
            _session = None
            return new_response(result = apiresults["SUCCESS"])
    
        case "update_chart":
            if _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])
            
            try:
                for element in data["changes"]:
                    new_element_as_object = object_from_dict(element)
                    
                    if new_element_as_object is None:
                        return new_response(result = apiresults["BAD_DATA"], error_info = "Could not convert dict {} to an xml wrapper class".format(element))
                    
                    diff = []
                    result = update_chart_diff(_session.chart_instance, new_element_as_object, remove = not element["exists"], diff = diff)
                    
                    if result == Result.SUCCESS:
                        return new_response(result = apiresults["SUCCESS"], diff = diff) 
            except KeyError:
                return new_response(result = apiresults["BAD_DATA"]) 
   
        case "get_steps":
            if _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])

            steps = []
            for element in _session.chart_instance.sequence_data:
                steps.append(dict_from_object(element))

            return new_response(result = apiresults["SUCCESS"], steps = steps)
        
        case "get_bpms":
            if _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])

            bpms = []
            for element in _session.chart_instance.info.bpm_info:
                bpms.append(dict_from_object(element))

            return new_response(result = apiresults["SUCCESS"], bpms = bpms)

        case "get_measures":
            if _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])

            measures = []
            for element in _session.chart_instance.info.measure_info:
                measures.append(dict_from_object(element))

            return new_response(result = apiresults["SUCCESS"], measures = measures)


        case "introspect_has_session":
            if _session is None:
                return new_response(result = apiresults["FALSE"])
            return new_response(result = apiresults["TRUE"])

    return new_response(result = apiresults["INVALID_FUNCTION"], error_info = head["function"])
