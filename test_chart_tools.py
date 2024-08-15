from chart_tools import *
from common import *
import xml.etree.ElementTree
import sys
import unittest
import subprocess
import shutil
import hashlib

testchart1md5sum = "700d0b414fbcfdb42c38b656b9672d6f"

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

#Generate a chart with 92 beats of left foot steps on every beat, alternating back and forth in position, starting at the 8th beat
def makeDummyChart():
    testChart = Chart(endTick = beatsToTicks(120, 480))

    testChart.addBPM(BPM(bpm = 121), 0)

    noteSize = sizeUnit(int(65536 / 4))

    for i in range(8, 100):
        testChart.addNote(noteSize, getPosition(noteSize, (65536 / 4) + ((i % 2) * (65536 / 4))), i, PlayerID.PLAYER1, StepTypes.LEFT)

    return testChart


#Generate a chart testing every element that we can create
def makeCompleteChart():
    testChart = Chart(endTick = beatsToTicks(120, 480))

    testChart.addBPM(BPM(bpm = 121), 0)

    noteSize = sizeUnit(int(65536/4))

    currentBeat = 4

    locationLeft = getPosition(noteSize, 65535/4)
    locationRight = getPosition(noteSize, 2*(65535/4))

    #Four alternating stpes on every other beat 
    for i in range(0, 8, 2):
        if i % 4 == 0:
            testChart.addNote(noteSize, getPosition(noteSize, (65536 / 4) + ((i % 4) * (65536 / 4))), currentBeat, PlayerID.PLAYER1, StepTypes.LEFT)
        elif i % 2 == 0:
            testChart.addNote(noteSize, getPosition(noteSize, (65536 / 4) + ((i % 2) * (65536 / 4))), currentBeat, PlayerID.PLAYER1, StepTypes.RIGHT)
        currentBeat += 1

    currentBeat += 2

    #A left foot hold and then right foot hold for 2 beats each
    leftStep = testChart.addNote(noteSize, locationLeft, currentBeat, PlayerID.PLAYER1, StepTypes.LEFT)
    testChart.addLongPoint(leftStep, beatsToTicks(2, testChart.timeUnit))
    
    currentBeat += 2
    
    rightStep = testChart.addNote(noteSize, locationRight, currentBeat, PlayerID.PLAYER1, StepTypes.RIGHT)
    testChart.addLongPoint(rightStep, beatsToTicks(2, testChart.timeUnit))

    #A left foot hold for 1 beat that slides right on the 2nd beat, then the opposite of that
    currentBeat += 2
    
    leftStep = testChart.addNote(noteSize, locationLeft, currentBeat, PlayerID.PLAYER1, StepTypes.LEFT)
    testChart.addLongPoint(leftStep, beatsToTicks(1, testChart.timeUnit)) 
    pointToMove = testChart.addLongPoint(leftStep, beatsToTicks(1, testChart.timeUnit))
    testChart.movePoint(leftStep, pointToMove, locationRight)

    currentBeat += 2
    
    rightStep = testChart.addNote(noteSize, locationRight, currentBeat, PlayerID.PLAYER1, StepTypes.RIGHT)
    testChart.addLongPoint(rightStep, beatsToTicks(1, testChart.timeUnit))
    pointToMove = testChart.addLongPoint(rightStep, beatsToTicks(1, testChart.timeUnit))
    testChart.movePoint(rightStep, pointToMove, locationLeft)

    #A left foot hold for 1 beat terminating in a right swipe, a right foot hold for 1 beat terminating in a left swipe
    currentBeat += 2
    
    leftStep = testChart.addNote(noteSize, locationLeft, currentBeat, PlayerID.PLAYER1, StepTypes.LEFT)
    pointToSwipe = testChart.addLongPoint(leftStep, beatsToTicks(1, testChart.timeUnit)) 
    testChart.addSwipe(leftStep, pointToSwipe, locationRight) 

    currentBeat += 2
    
    rightStep = testChart.addNote(noteSize, locationRight, currentBeat, PlayerID.PLAYER1, StepTypes.RIGHT)
    pointToSwipe = testChart.addLongPoint(rightStep, beatsToTicks(1, testChart.timeUnit))
    testChart.addSwipe(rightStep, pointToSwipe, locationLeft)

    #A jump
    currentBeat += 2

    testChart.addJump(beatsToTicks(currentBeat, testChart.timeUnit))

    #A down
    currentBeat += 2
    testChart.addDown(beatsToTicks(currentBeat, testChart.timeUnit))
    
    return testChart

def generateTestChart():
    testChart = makeDummyChart()

    testChart.save("testchart1.xml")


def generateCompleteChart():
    testChart = makeCompleteChart()
    testChart.save("completechart1.xml")


class TestChartXMLInterface(unittest.TestCase):
    def testbpmInfoXMLRemoveBPM(self):
        testChart = makeDummyChart()

        self.assertEqual(testChart.xml.info.bpm_info.removeAtIndex(500), Result.INVALID_INDEX, "Invalid bpm index can't be removed")
        self.assertEqual(testChart.xml.info.bpm_info.removeAtIndex(0), Result.SUCCESS, "Valid bpm index can be removed")

    def testmeasureInfoRemoveMeasure(self):
        testChart = makeDummyChart()

        self.assertEqual(testChart.xml.info.measure_info.removeAtIndex(500), Result.INVALID_INDEX, "Invalid measure index can't be removed")
        self.assertEqual(testChart.xml.info.measure_info.removeAtIndex(0), Result.SUCCESS, "Valid measure index can be removed")

    #Remove every other step from a chart
    def testsequenceDataRemoveSteps(self):
        testChart = makeDummyChart()

        i = 0
        stepsToRemove = []
        for step in testChart.xml.sequence_data:
            if i % 2 == 1:
                stepsToRemove.append(step)
            i += 1

        for step in stepsToRemove:
            testChart.xml.sequence_data.remove(step)

            #Verify that we removed the correct element
            self.assertEqual((step not in testChart.steps), True)

        self.assertEqual(len(testChart.xml.sequence_data), int(92/2), "Removing every other note leaves 46 notes")


class TestCharts(unittest.TestCase):
    def testTestChart1(self):
        with open("testchart1.xml", "rb") as file:
            md5out = hashlib.md5(file.read()).hexdigest()

            self.assertEqual(md5out, testchart1md5sum, "testchart1.xml checksum == expected checksum")


if __name__ == "__main__":
    generateCompleteChart()
    generateTestChart()
    unittest.main()
