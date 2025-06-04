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
    - Under construction
    - Flask app to expose this functionality through an api
