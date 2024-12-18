from chart_tools import *
from common import *
#from chart_tools_api import *
import chart_tools_api

import xml.etree.ElementTree
import sys
import unittest
import subprocess
import shutil
import hashlib

testchart1md5sum = "b658ba41ebd45383617d91d59e83ed6b"

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
        testChart.addNote(getPosition(noteSize, (65536 / 4) + ((i % 2) * (65536 / 4))), beatsToTicks(i, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.LEFT)

    return testChart


#Generate a chart testing every element that we can create
def makeCompleteChart():
    testChart = Chart(endTick = beatsToTicks(120, 480))

    testChart.addBPM(BPM(bpm = 121), 0)

    noteSize = sizeUnit(int(65536/4))

    currentBeat = 8
    
    locationLeft = getPosition(noteSize, 65535/4)
    locationRight = getPosition(noteSize, 2*(65535/4))

    #Four alternating stpes on every other beat 
    for i in range(0, 8, 2):
        if i % 4 == 0:
            testChart.addNote(getPosition(noteSize, (65536 / 4) + ((i % 4) * (65536 / 4))), beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.LEFT)
        elif i % 2 == 0:
            testChart.addNote(getPosition(noteSize, (65536 / 4) + ((i % 2) * (65536 / 4))), beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.RIGHT)
        currentBeat += 1

    currentBeat += 2

    #A left foot hold and then right foot hold for 2 beats each
    leftStep = testChart.addNote(locationLeft, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.LEFT)
    testChart.addLongPoint(leftStep, beatsToTicks(2, testChart.timeUnit))
    
    currentBeat += 2
    
    rightStep = testChart.addNote(locationRight, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.RIGHT)
    testChart.addLongPoint(rightStep, beatsToTicks(2, testChart.timeUnit))

    #A left foot hold for 1 beat that slides right on the 2nd beat, then the opposite of that
    currentBeat += 2
    
    leftStep = testChart.addNote(locationLeft, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.LEFT)
    testChart.addLongPoint(leftStep, beatsToTicks(1, testChart.timeUnit)) 
    pointToMove = testChart.addLongPoint(leftStep, beatsToTicks(1, testChart.timeUnit))
    testChart.movePoint(leftStep, pointToMove, locationRight)

    currentBeat += 2
    
    rightStep = testChart.addNote(locationRight, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.RIGHT)
    testChart.addLongPoint(rightStep, beatsToTicks(1, testChart.timeUnit))
    pointToMove = testChart.addLongPoint(rightStep, beatsToTicks(1, testChart.timeUnit))
    testChart.movePoint(rightStep, pointToMove, locationLeft)

    #A left foot hold for 1 beat terminating in a right swipe, a right foot hold for 1 beat terminating in a left swipe
    currentBeat += 2
    
    leftStep = testChart.addNote(locationLeft, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.LEFT)
    pointToSwipe = testChart.addLongPoint(leftStep, beatsToTicks(1, testChart.timeUnit)) 
    testChart.addSwipe(leftStep, pointToSwipe, locationRight) 

    currentBeat += 2
    
    rightStep = testChart.addNote(locationRight, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.RIGHT)
    pointToSwipe = testChart.addLongPoint(rightStep, beatsToTicks(1, testChart.timeUnit))
    testChart.addSwipe(rightStep, pointToSwipe, locationLeft)

    #A jump
    currentBeat += 2

    testChart.addJump(beatsToTicks(currentBeat, testChart.timeUnit))

    #A down
    currentBeat += 2
    testChart.addDown(beatsToTicks(currentBeat, testChart.timeUnit))

    effectDuration = 8

    #Effects
    #We'll add a step to each one to visually delineate where each one begins
   
    for layer in layerNameValues:
        currentBeat += effectDuration
        if layerNameValues[layer][0] == "Background":
            testChart.addEffect(layer, beatsToTicks(currentBeat, testChart.timeUnit), 2, r = 255, g = 255, b = 255)
        elif layerNameValues[layer][0] == "OverEffect":
            testChart.addEffect(layer, beatsToTicks(currentBeat, testChart.timeUnit), 4)
        else:
            testChart.addEffect(layer, beatsToTicks(currentBeat, testChart.timeUnit), 2)
           
        noteSize = noteCoordinates()
        noteSize.left = noteCoordinates.MIN
        noteSize.right = noteCoordinates.MAX

        testChart.addNote(noteSize, beatsToTicks(currentBeat, testChart.timeUnit), PlayerID.PLAYER1, StepTypes.LEFT)


    #one last note so the chart doesn't end before the effects 
    currentBeat += effectDuration
    testChart.addJump(beatsToTicks(currentBeat, testChart.timeUnit))
    
    return testChart

#Can we add effects that start on the expected beat?/
def generateEffectSyncTest():
    testChart = Chart() 

    testChart.addBPM(BPM(bpm = 121), 0)

    for i in range(0, 200, 4):
    
        testChart.addJump(beatsToTicks(i, testChart.timeUnit))
       
        if i % 8 == 0:
            testChart.addEffect("sp3_led_01", beatsToTicks(i, testChart.timeUnit), 4, r = 255, g = 255, b = 255)
        else:
            testChart.addEffect("sp3_led_11", beatsToTicks(i, testChart.timeUnit), 4, r = 255, g = 255, b = 255)

    testChart.save("effectsynctest.xml")

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
    def testsequenceDataRemoveSteps_XML(self):
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

    #Test element removals by value (ie how it works when we do it through the api)
    def testRemoveByValue(self):
        testChart = makeDummyChart()

        removeStep = stepXML(createEmptyStepXML())
        removeStep.start_tick = 4800
        removeStep.end_tick = 4800
        removeStep.left_pos = 16384
        removeStep.right_pos = 32768
        removeStep.kind = 1
        removeStep.player_id = 0

        self.assertEqual(testChart.steps[2].start_tick, removeStep.start_tick)
        self.assertEqual(testChart.steps[2], removeStep)
        self.assertEqual(testChart.removeNote(removeStep), Result.SUCCESS, "start_tick " + str(removeStep.start_tick) + " " + str(testChart.steps[2].start_tick) + " end_tick " + str(removeStep.end_tick) + " " + str(testChart.steps[2].end_tick) + " left_pos " + str(removeStep.left_pos) + " " +  str(testChart.steps[2].left_pos) + " right_pos " + str(removeStep.right_pos) + " " + str(testChart.steps[2].right_pos) + " kind " + str(removeStep.kind) + " " + str(testChart.steps[2].kind) + " player_id " + str(removeStep.player_id) + " " + str(testChart.steps[2].player_id))
        self.assertNotEqual(testChart.steps[2].start_tick, removeStep.start_tick)

        #make sure we cant remove an invalid BPM
        badBPM = bpmXML(createEmptyBPMXML())
        badBPM.tick = 0
        badBPM.bpm = 12345
        self.assertEqual(testChart.removeBPM(badBPM), Result.NO_ACTION)
        
        badBPM.bpm = 12100
        badBPM.tick = 100
        self.assertEqual(testChart.removeBPM(badBPM), Result.NO_ACTION)

        #remove a BPM
        newBPM = bpmXML(createEmptyBPMXML())
        newBPM.tick = 0
        newBPM.bpm = 12100
        self.assertEqual(testChart.removeBPM(newBPM), Result.SUCCESS)
        self.assertEqual(len(testChart.xml.info.bpm_info), 0)
        
        #cant remove invalid measure
        badMeasure = measureXML(createEmptyMeasureXML())
        badMeasure.tick = 10
        badMeasure.num = 5
        badMeasure.denomi = 4

        self.assertEqual(testChart.removeMeasure(badMeasure), Result.NO_ACTION)

        newMeasure = measureXML(createEmptyMeasureXML())
        newMeasure.tick = 0
        newMeasure.num = 4
        newMeasure.denomi = 4

        self.assertEqual(testChart.removeMeasure(newMeasure), Result.SUCCESS)
        self.assertEqual(len(testChart.xml.info.measure_info), 0)

        #add a long point, then remove it
        testChart.addLongPoint(testChart.steps[4], 100)
        self.assertEqual(len(testChart.steps[4].long_point), 1)
        
        #can't remove valid long_point when the step doesn't exist in the chart
        badStep = stepXML(createEmptyStepXML())
        badStep.start_tick = 10
        badStep.end_tick = 10
        badStep.left_pos = 10
        badStep.right_pos = 10
        badStep.kind = 1
        badStep.player_id = 0

        self.assertEqual(testChart.removeLongPoint(badStep, testChart.steps[4].long_point[0]), Result.NOTE_DOESNT_EXIST)

        #can't remove invalid point
        badPoint = pointXML(createEmptyPointXML())
        badPoint.tick = 10
        badPoint.left_pos = 10
        badPoint.right_pos = 10

        self.assertEqual(testChart.removeLongPoint(testChart.steps[4], badPoint), Result.NO_ACTION)
        self.assertEqual(len(testChart.steps[4].long_point), 1)

        #remove valid point
        self.assertEqual(testChart.removeLongPoint(testChart.steps[4], testChart.steps[4].long_point[0]), Result.SUCCESS)
        self.assertEqual(len(testChart.steps[4].long_point), 0)


class TestCharts(unittest.TestCase):
    def testTestChart1(self):
        with open("testchart1.xml", "rb") as file:
            md5out = hashlib.md5(file.read()).hexdigest()

            self.assertEqual(md5out, testchart1md5sum, "testchart1.xml checksum == expected checksum")


    def testAPI(self):
        session = chart_tools_api.Session()

        command = chart_tools_api.parse_command("chart load testchart1.xml")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        self.assertIsNotNone(session.chart)

        command = chart_tools_api.parse_command("bpm add 57300 0")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)

        command = chart_tools_api.parse_command("bpm remove 57300 0")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        
        command = chart_tools_api.parse_command("note add 100 100 100 200 1 0")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        
        command = chart_tools_api.parse_command("note remove 100 100 100 200 1 0")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
      
        command = chart_tools_api.parse_command("measure add 4 4 10")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        
        command = chart_tools_api.parse_command("measure remove 4 4 10")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        
        command = chart_tools_api.parse_command("chart save apisavetest.xml")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        
        command = chart_tools_api.parse_command("chart get")
        chartResponse = chart_tools_api.dispatch_command(command, session)
        self.assertEqual(chartResponse.split('\n')[0], "note 3840 3840 16384 32768 1 0", "First line of api 'chart get' response")

        #sanity check
        self.assertFalse(session.chart.steps[-1].start_tick == 100)

        #long points
        command = chart_tools_api.parse_command("note add 100 100 100 200 1 0")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
      
        #adding a valid hold works (tick at 100, same as the parent note)
        command = chart_tools_api.parse_command("hold add 100 100 100 200 1 0 200 100 200")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
        
        #make sure it added correctly
        self.assertEqual(session.chart.steps[-1].start_tick, 100)
        self.assertEqual(len(session.chart.steps[-1].long_point), 1)
        self.assertEqual(session.chart.steps[-1].long_point[0].tick, 200)

        #adding an invalid hold (time earlier than last tick in the note) does not work
        command = chart_tools_api.parse_command("hold add 100 200 100 200 1 0 100 100 200")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.TIME_OUT_OF_BOUNDS, command.unparsed)

        #adding another correct one does work
        command = chart_tools_api.parse_command("hold add 100 200 100 200 1 0 300 100 200")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)

        #removing one
        command = chart_tools_api.parse_command("hold remove 100 300 100 200 1 0 300 100 200")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)
       
        #sanity check
        self.assertEqual(len(session.chart.steps[-1].long_point), 1)

        command = chart_tools_api.parse_command("note remove 100 300 100 200 1 0")
        self.assertEqual(chart_tools_api.dispatch_command(command, session), Result.SUCCESS, command.unparsed)

    def testCommandLine(self):
        commandline = "python3.12 chart_tools_api.py init testyy.xml : bpm add 57300 0"

if __name__ == "__main__":
    generateCompleteChart()
    generateTestChart()
    generateEffectSyncTest()

    unittest.main()
