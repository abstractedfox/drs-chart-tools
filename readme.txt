DRS Chart Tools: Tools for modifying chart and music database data for Dancerush Stardom.

#### This project is undergoing a deep refactor! The old (outdated) readme follows for posterity.

Presently this is really only something that would be useful to a programmer; there is no interface for a typical user to start making their own charts yet.

chart_tools.py: Functions to modify a dancerush chart. Mostly just handles putting xml elements where they belong and error checking that values are within appropriate bounds. Capable of modifying existing charts and generating empty ones.

chart_tools_api.py (Incomplete) Not an API over, say, TCP, but it could be if you want it to do that. Really just exposes everything chart_tools.py does through stdout/in. Uses short commands to direct it to load, modify, and save charts.

chart_xml_interface.py: The part that actually touches the XML, really just an interface to ElementTree elements that lets you use them a little more pythonically

database_tools.py: Analog to chart_xml_interface.py, plus some useful functions for database modiciation (some of these should be split off into a new file when we make one more purpose built beyond just handling xml)

./notes/: Observations from studying the formats, no guarantee that these will be readable to anyone but me

More detailed usage below

chart_tools_api.py
The first two args are the infile and outfile. To generate an empty chart, write 'init' instead of an input filename.
Individual commands are formatted as:
(the attribute to modify) (the thing to do to that attribute) (any subsequent arguments that may be specific to that command)
Subsequent commands are separated by a ':' character.
available commands:
note (add, remove) (start tick) (end tick) (left pos) (right pos) (note type as 1, 2, 3, 4 for left, right, down, jump) (player_id as 0, 1, 4 for p1, p2, (convention for all jump/downs))
    -When removing, it will remove the first note it finds that matches all of the attributes passed
bpm (add, remove) (BPM value) (tick)
    -Unlike in the actual XML chart, decimal values for the BPM should be formatted with an actual decimal (ie 150 for 150bpm, 150.05 for 150.05bpm)
measure (add, remove) numerator denominator tick
hold (add, remove) (all arguments for parent step, matching same order as the command for 'note') tick left_pos right_pos
    -First five args must match an existing note in the chart to be the parent note for the hold
Example of how commands should be formatted:
python3.12 chart_tools_api.py init test_chart_new.xml bpm add 150 0 : measure add 4 4 0 : note add 0 0 1000 6000 1 0 : note add 100 1000 1000 2000 1 0 : hold add 100 1000 1000 2000 1 0 100 1000 2000
    -Create a dummy chart with a bpm of 150 starting at tick 0, measure of 4/4 starting at tick 0, a left foot step with dimensions (1000, 6000) for p1 at tick 0, a left foot step with dimensions (1000, 2000) for player 1 at tick 100, and a left foot hold note step from tick 100 to 1000 with starting dimensions (1000, 2000) for player 1 starting at tick 100 with ending dimensions 1000, 2000




