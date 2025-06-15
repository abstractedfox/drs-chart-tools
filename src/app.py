from warnings import warn

from runtime import *

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost/"}})
cors = CORS(app, resources={r"*": {"origins": "*"}})

_session = None
_sessions = {}

apiresults = {
    "UNDEFINED": "UNDEFINED",
    "BAD_REQUEST": "BAD_REQUEST",
    "BAD_DATA": "BAD_DATA",
    "NOT_INITIALIZED": "NOT_INITIALIZED",
    "SUCCESS": "SUCCESS",
    "TRUE": "TRUE",
    "FALSE": "FALSE",
    "INVALID_FUNCTION": "INVALID_FUNCTION",
    "FAILED": "FAILED",
    "INVALID_SESSION": "INVALID_SESSION",
}

def new_response(result = apiresults["UNDEFINED"], error_info = None, diff = [], steps = [], bpms = [], measures = [], session_ID = None, raw_chart = None):
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

    if session_ID:
        response["head"]["id"] = session_ID

    if raw_chart:
        response["data"]["raw_chart"] = raw_chart

    return response 

#Request reference, also useful for testing
def new_request(function = "", data = {}, changes = [], filename = None, session_ID = None, raw_chart = None):
    request = {"head": {"function": function}, "data": data}

    #implementations shouldn't make this optional
    if session_ID:
        request["head"]["id"] = session_ID
    
    match function:
        case "init":
            data["filename"] = filename
            if raw_chart:
                data["raw_chart"] = raw_chart

        case "save":
            pass
        
        case "close_session":
            pass

        case "update_chart":
            data["changes"] = changes

        case "get_steps":
            pass

        case "get_bpms":
            pass

        case "get_measures":
            pass

        case "introspect_has_session":
            pass

    return request

#TODO: Once tests are changed to reflect the change to multiple sessions, get rid of _session and clean up any code that handles switching _session and _sessions
@app.route("/api", methods=["POST"])
def api():
    global _session
    global _sessions

    #log("Received request: {}".format(request.json))
    if "head" not in request.json:
        response = new_response()
        verifydict(response["head"])["result"] = apiresults["BAD_REQUEST"] 
        return response
   
    head = request.json["head"]
    data = request.json["data"]
    session_ID = None
    if "id" in head and head["function"] != "init":
        session_ID = head["id"]
    
    match head["function"]:
        case "init":
            if "raw_chart" in data:
                with open(data["filename"], "w") as newchart:
                    newchart.write(data["raw_chart"])
            
            new_session = Session(path = data["filename"])
            _sessions[new_session.ID] = new_session
            
            #scaffolding to avoid breaking old tests (delete once old tests no longer expect a single session)
            _session = [_sessions[s] for s in _sessions][-1]
    
            return new_response(result = apiresults["SUCCESS"], session_ID = new_session.ID)

        case "save":
            if session_ID:
                result = _sessions[session_ID].save()
            else:
                result = _session.save() 

            if result == Result.SUCCESS:
                return new_response(result = apiresults["SUCCESS"])
            else:
                return new_response(result = apiresults["FAILED"], error_info = result.name)

        case "close_session":
            if session_ID:
                try:
                    _sessions.pop(session_ID)
                except KeyError:
                    return new_response(result = apiresults["INVALID_SESSION"])
            else:
                _session = None
            
            return new_response(result = apiresults["SUCCESS"])
    
        case "update_chart":
            current_session = None
            if session_ID:
                if session_ID not in _sessions:
                    return new_response(result = apiresults["INVALID_SESSION"])
                current_session = _sessions[session_ID]
            elif _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])
            else:
                current_session = _session

            try:
                for element in data["changes"]:
                    new_element_as_object = object_from_dict(element)
                    
                    if new_element_as_object is None:
                        return new_response(result = apiresults["BAD_DATA"], error_info = "Could not convert dict {} to an xml wrapper class".format(element))
                    
                    diff = []
                    result = update_chart_diff(current_session.chart_instance, new_element_as_object, remove = not element["exists"], diff = diff)
                    
                    if result == Result.SUCCESS:
                        return new_response(result = apiresults["SUCCESS"], diff = diff) 
                    else:
                        return new_response(result = apiresults["FAILED"], error_info = result.name)
            except KeyError:
                return new_response(result = apiresults["BAD_DATA"]) 
   
        case "get_steps":
            current_session = None
            if session_ID:
                if session_ID not in _sessions:
                    return new_response(result = apiresults["INVALID_SESSION"])
                current_session = _sessions[session_ID]
            elif _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])
            else:
                current_session = _session

            steps = []
            for element in current_session.chart_instance.sequence_data:
                steps.append(dict_from_object(element))

            if len(steps) == 0:
                warn("get_steps called with zero steps, session_ID = {}".format(session_ID), RuntimeWarning)

            return new_response(result = apiresults["SUCCESS"], steps = steps)
        
        case "get_bpms":
            current_session = None
            if session_ID:
                if session_ID not in _sessions:
                    return new_response(result = apiresults["INVALID_SESSION"])
                current_session = _sessions[session_ID]
            elif _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])
            else:
                current_session = _session

            bpms = []
            for element in current_session.chart_instance.info.bpm_info:
                bpms.append(dict_from_object(element))

            return new_response(result = apiresults["SUCCESS"], bpms = bpms)

        case "get_measures":
            current_session = None
            if session_ID:
                if session_ID not in _sessions:
                    return new_response(result = apiresults["INVALID_SESSION"])
                current_session = _sessions[session_ID]
            elif _session is None:
                return new_response(result = apiresults["NOT_INITIALIZED"])
            else:
                current_session = _session

            measures = []
            for element in _session.chart_instance.info.measure_info:
                measures.append(dict_from_object(element))

            return new_response(result = apiresults["SUCCESS"], measures = measures)

        #Note that at present this gets the chart _as it exists on disk_! You have to call to save it first!
        case "get_raw_chart":
            if session_ID not in _sessions:
                return new_response(result = apiresults["INVALID_SESSION"])

            with open(_sessions[session_ID].path) as chart:
                return new_response(result = apiresults["SUCCESS"], raw_chart = chart.read())

        case "introspect_has_session":
            if _session is None and len(_sessions) == 0:
                return new_response(result = apiresults["FALSE"])
            return new_response(result = apiresults["TRUE"])

    return new_response(result = apiresults["INVALID_FUNCTION"], error_info = head["function"])
