from chart_tools import *
import xml.etree.ElementTree
import sys
import unittest

#note to self: make sure we test whether len() works on the bpmInfo class implicitly when you overload []

def testXMLInterface():
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

def makeDummyChart():
    testChart = Chart(endTick = beatsToTicks(120, 480))

    testChart.addBPM(BPM(bpm = 121), 0)

    noteSize = sizeUnit(int(65536 / 4))

    for i in range(8, 100):
        testChart.addNote(noteSize, getPosition(noteSize, (65536 / 4) + ((i % 2) * (65536 / 4))), i, PlayerID.PLAYER1)

    return testChart

def generateTestChart():
    testChart = makeDummyChart()

    testChart.save("testchart.xml")


class TestChartXMLInterface(unittest.TestCase):
    def testChartXMLInterface():
        pass

generateTestChart()
