from runtime import *

from flask import Flask, jsonify, request

app = Flask(__name__)

session = None

def new_response():
    return {"head": {"result": ""}}

apiresults = {
    "BAD_REQUEST": "BAD_REQUEST",
    "SUCCESS": "SUCCESS"
}

@app.route("/api", methods=["POST"])
def api():
    log("Received request: {}".format(request.json))
    if "head" not in request.json:
        response = new_response()
        verifydict(response["head"])["result"] = apiresults["BAD_REQUEST"] 
        return response
   
    head = request.json["head"]
    data = request.json["data"]
    match head["function"]:
        case "init":
            session = Session(path = data["filename"]) 
            
            response = new_response()
            verifydict(response["head"])["result"] = apiresults["SUCCESS"]
            
            return response 
    
    return {}
