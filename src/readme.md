Quick refactor docs so I can keep track of what's going on here

At present, we have:
- chart_xml_interface.py
    - An interface to the xml files. Avoids having ugly ElementTree code everywhere/interfacing with the files more pythonically
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
`{ 
    "head": 
        {
            "function": __mandatory__ *function being called*
                *possible values: init, save, close_session, update_chart, get_steps, get_bpms, get_measures, introspect_has_session*
        },
    "data":
        {
            "filename": __only when calling init__ *filename (or path) to be used on initialization*
            "changes": __only when calling update_chart__ *chart elements as json obejcts*
        }
}`

Responses look like:
`{ 
    "head": 
        {
            "result": __always__ *status of the operation*
        },
    "data":
        {
            "error_info": __sometimes__ *may contain extra data about some errors*,
            "steps": __sometimes__ *steps returned after a call to get_steps*,
            "bpms": __sometimes__ *bpms returned after a call to get_bpms*,
            "measures": __sometimes__,
            "diff": __sometimes__ *The diff after an operation that modifies the chart*
        }
}`
