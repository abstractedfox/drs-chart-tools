Quick refactor docs so I can keep track of what's going on here

At present, we have:
- chart_xml_interface.py
    - An interface to the xml files. Avoids having ugly ElementTree code everywhere/allows interfacing with the files more pythonically
    - Usage pattern is that the wrapper classes interface with an *existing* xml tag. There are separate factory functions to create new instances of xml tags
- chart_tools.py
    - Use update_chart function to add or remove things from a chart instance (as chartRootXML) in a declarative fashion. Will not add duplicate elements and gracefully handles attempts to remove elements that don't exist
    - Otherwise, contains functions for casting between wrapper class instances (from chart_xml_interface) and dicts (to be used by the json parser for the API) 
- runtime.py
    - Everything has been stateless until here. This file just provides a small class that says, 'I am statefully holding a chart!'
- app.py
    - Flask app to expose this functionality through an api
    - Contains a reference implementation of a function for building requests
    

#### API reference:
Requests should be JSON objects that look like:
```
{ 
    "head": 
        {
            "function": /*mandatory*/ "name of function",
                /*possible values: init, save, close_session, update_chart, get_steps, get_bpms, get_measures, introspect_has_session, parse_chart*/
            [DEPRECATED AS OF V3] "id": /*mandatory, except when calling 'init'*/ "session ID",
        },
    "data":
        {
            [DEPRECATED AS OF V3] "filename": /*only when calling init*/ "filename (or path) to be used on initialization"
            "changes": /*only when calling update_chart (pre V3) or process_to_xml (V3) */ "chart elements as json objects"
        }
}
```

Responses look like:
```
{ 
    "head": 
        {
            "result": /*always*/ "status of the operation",
            [DEPRECATED AS OF V3] "id": /*always*/ "id of the session affected"
        },
    "data":
        {
            "error_info": /*sometimes, may contain extra data about some errors */,
            "steps": /*sometimes, steps returned after a call to get_steps*/,
            "bpms": /*sometimes, bpms returned after a call to get_bpms*/,
            "measures": /*sometimes*/,
            [DEPRECATED AS OF V3] "diff": /*sometimes, the diff after an operation that modifies the chart*/
        }
}
```

Dicts representing chart elements contain all the relevant fields as in the original XML by the same name (impl. note: do not change this) but also include a "type" field indicating what kind of element they are (ie a bpm dict has type "bpm_info", step dict has type "step", measure dict has type "measure_info") 

Note that step long point dicts contain None (python) or null (javascript) for *_end_pos parameters if they don't exist

Usage pattern (V3):
V3 is even more stateless™, which actually makes it a lot simpler to use!
* `parse_chart` accepts an XML chart, as text, in `data["raw_chart"]`, and returns the entire chart as dicts in `data["steps"]`, `data["bpms"]`, and `data["measures"]`
* `process_to_xml` accepts dicts in data["changes"] and returns the chart as XML

