from chart_tools import *
import xml.etree.ElementTree
import sys

#note to self: make sure we test whether len() works on the bpmInfo class implicitly when you overload []

fumen = xml.etree.ElementTree.parse(sys.argv[1])

testChartInfo = chartInfo(fumen.getroot())

print(testChartInfo.time_unit)
print(testChartInfo.end_tick)
print("bpm 0 tick: " + testChartInfo.bpm_info[0].tick)
print("bpm 0 bpm: " + testChartInfo.bpm_info[0].bpm)
print("measure 0 tick: " + testChartInfo.measure_info[0].tick)
print("measure 0 num: " + testChartInfo.measure_info[0].num)
print("measure 0 denomi: " + testChartInfo.measure_info[0].denomi)

sequenceTest = sequence_data(fumen.getroot().find("sequence_data"))

print("step 0 start_tick: " + sequenceTest.sequence_data[0].start_tick)
print("step 0 end_tick: " + sequenceTest.sequence_data[0].end_tick)
print("step 0 left_pos: " + sequenceTest.sequence_data[0].left_pos)
print("step 0 right_pos: " + sequenceTest.sequence_data[0].right_pos)
print("step 0 kind: " + sequenceTest.sequence_data[0].kind)
print("step 0 player_id: " + sequenceTest.sequence_data[0].player_id)
