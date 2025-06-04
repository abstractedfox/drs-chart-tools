Quick refactor docs so I can keep track of what's going on here

At present, we have:
- chart_xml_interface.py
    - An interface to the xml files. Avoids having ugly ElementTree code everywhere/allows interfacing with the files more pythonically
    - Usage pattern is that the wrapper classes interface with an *existing* xml tag. There are separate factory functions to create new instances of xml tags
- chart_tools_new.py
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
            "function": /*mandatory*/ "name of function"
                /*possible values: init, save, close_session, update_chart, get_steps, get_bpms, get_measures, introspect_has_session*/
        },
    "data":
        {
            "filename": /*only when calling init*/ "filename (or path) to be used on initialization"
            "changes": /*only when calling update_chart*/ "chart elements as json objects"
        }
}
```

Responses look like:
```
{ 
    "head": 
        {
            "result": /*always*/ "status of the operation"
        },
    "data":
        {
            "error_info": /*sometimes, may contain extra data about some errors */,
            "steps": /*sometimes, steps returned after a call to get_steps*/,
            "bpms": /*sometimes, bpms returned after a call to get_bpms*/,
            "measures": /*sometimes*/,
            "diff": /*sometimes, the diff after an operation that modifies the chart*/
        }
}
```
