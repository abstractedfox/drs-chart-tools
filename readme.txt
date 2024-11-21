DRS Chart Tools: Tools for modifying chart and music database data for Dancerush Stardom.

Presently this is really only something that would be useful to a programmer; there is no interface for a typical user to start making their own charts yet.

chart_tools.py: Functions to modify a dancerush chart. Mostly just handles putting xml elements where they belong and error checking that values are within appropriate bounds. Capable of modifying existing charts and generating empty ones.

chart_tools_api.py (Incomplete) Not an API over, say, TCP, but it could be if you want it to do that. Really just exposes everything chart_tools.py does through stdout/in.

chart_xml_interface.py: The part that actually touches the XML, really just an interface to ElementTree elements that lets you use them a little more pythonically

database_tools.py: Analog to chart_xml_interface.py, plus some useful functions for database modiciation (some of these should be split off into a new file when we make one more purpose built beyond just handling xml)
