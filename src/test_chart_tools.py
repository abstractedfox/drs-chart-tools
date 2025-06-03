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

#post refactor imports
from chart_tools_new import *

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

class TestChartToolsNew(unittest.TestCase):
    def test_dict_factory(self):
        bpmdict = new_bpm_info_dict(bpm = 100)
        self.assertIsNotNone(bpmdict)
        [self.assertTrue(x in ["exists", "type", "tick", "bpm"]) for x in bpmdict]
        self.assertEqual(len(bpmdict), 4)
        self.assertEqual(bpmdict["bpm"], 100)

    def test_object_from_dict(self):
        bpmdict = new_bpm_info_dict(bpm = 100)
        result = object_from_dict(bpmdict)
        self.assertEqual(type(result), bpmXML)
        self.assertEqual(result.bpm, 100)
    
        measuredict = new_measure_info_dict(num = 4, denomi = 8)
        result = object_from_dict(measuredict)
        self.assertEqual(result.num, 4)
        self.assertEqual(result.denomi, 8)

        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        result = object_from_dict(stepdict)
        self.assertEqual(result.start_tick, 10)
        self.assertEqual(result.end_tick, 20)
        self.assertEqual(result.left_pos, 30)
        self.assertEqual(result.right_pos, 40)
        self.assertEqual(result.kind, 1)
        self.assertEqual(result.player_id, 1)

        pointdict = new_point_dict(tick = 10, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        result = object_from_dict(pointdict)
        self.assertEqual(result.tick, 10)
        self.assertEqual(result.left_pos, 20)
        self.assertEqual(result.right_pos, 30)
        self.assertEqual(result.left_end_pos, 40)
        self.assertEqual(result.right_end_pos, 50)

        #test a step which contains points
        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        pointdict = new_point_dict(tick = 10, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        pointdict2 = new_point_dict(tick = 100, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        stepdict["long_point"].append(pointdict)
        stepdict["long_point"].append(pointdict2)
        result = object_from_dict(stepdict)
        self.assertEqual(len(result.long_point), 2)
        self.assertEqual(type(result.long_point[0]), pointXML)
    
    def test_dict_from_object(self):
        bpmdict = new_bpm_info_dict(bpm = 100, tick = 200)
        classinstance = object_from_dict(bpmdict)
        dictagain = dict_from_object(classinstance)
        self.assertEqual(bpmdict, dictagain)
        
        measuredict = new_measure_info_dict(num = 4, denomi = 8)
        classinstance = object_from_dict(measuredict)
        dictagain = dict_from_object(classinstance)
        self.assertEqual(measuredict, dictagain)
        
        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        classinstance = object_from_dict(stepdict)
        dictagain = dict_from_object(classinstance)
        self.assertEqual(stepdict, dictagain)

        pointdict = new_point_dict(tick = 10, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        classinstance = object_from_dict(pointdict)
        dictagain = dict_from_object(classinstance)
        self.assertEqual(pointdict, dictagain)

        #step with points
        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        pointdict = new_point_dict(tick = 10, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        pointdict2 = new_point_dict(tick = 100, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        stepdict["long_point"].append(pointdict)
        stepdict["long_point"].append(pointdict2)
        classinstance = object_from_dict(stepdict)
        dictagain = dict_from_object(classinstance)
        self.assertEqual(stepdict, dictagain)


    def test_update_chart_step(self):
        #Can add a step
        chart = new_chart()
        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        step = object_from_dict(stepdict)
        self.assertEqual(update_chart(chart, step), Result.SUCCESS)
        self.assertEqual(len(chart.sequence_data), 1)

        #Can't add a step that is identical to an existing step 
        self.assertEqual(update_chart(chart, step), Result.NOTE_ALREADY_EXISTS)

        #Result.NO_ACTION when removing a step that doesn't exixt
        stepdict2 = new_step_dict(start_tick = 100, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        step2 = object_from_dict(stepdict2)
        self.assertEqual(update_chart(chart, step2, remove = True), Result.NO_ACTION)
        
        #Can remove a step 
        self.assertEqual(update_chart(chart, step, remove = True), Result.SUCCESS)
        self.assertEqual(len(chart.sequence_data), 0)

    #Test updating a chart with a step that contains points
    def test_update_chart_step_points(self):
        chart = new_chart()
        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        pointdict = new_point_dict(tick = 10, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        pointdict2 = new_point_dict(tick = 100, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        stepdict["long_point"].append(pointdict)
        stepdict["long_point"].append(pointdict2)
        step_object = object_from_dict(stepdict)
        update_chart(chart, step_object)
        self.assertEqual(len(chart.sequence_data[0].long_point), 2)
         

    def test_update_chart_measure(self):
        chart = new_chart()
        measuredict = new_measure_info_dict(num = 4, denomi = 8)
        measure = object_from_dict(measuredict)
        self.assertEqual(update_chart(chart, measure), Result.SUCCESS)
        self.assertEqual(len(chart.info.measure_info), 1)

        #Can't add a measure that is identical to an existing measure 
        self.assertEqual(update_chart(chart, measure), Result.MEASURE_ALREADY_EXISTS)

        #Result.NO_ACTION when removing a measure that doesn't exixt
        measuredict2 = new_measure_info_dict(num = 5, denomi = 8)
        measure2 = object_from_dict(measuredict2)
        self.assertEqual(update_chart(chart, measure2, remove = True), Result.NO_ACTION)
        
        #Can remove a measure 
        self.assertEqual(update_chart(chart, measure, remove = True), Result.SUCCESS)
        self.assertEqual(len(chart.sequence_data), 0)
         
    def test_update_chart_bpm(self):
        chart = new_chart()
        bpmdict = new_bpm_info_dict(bpm=100)
        bpm = object_from_dict(bpmdict)
        self.assertEqual(update_chart(chart, bpm), Result.SUCCESS)
        self.assertEqual(len(chart.info.bpm_info), 1)

        #Can't add a bpm that is identical to an existing bpm 
        self.assertEqual(update_chart(chart, bpm), Result.BPM_ALREADY_EXISTS)

        #Result.NO_ACTION when removing a bpm that doesn't exixt
        bpmdict2 =  new_bpm_info_dict(bpm=200)
        bpm2 = object_from_dict(bpmdict2)
        self.assertEqual(update_chart(chart, bpm2, remove = True), Result.NO_ACTION)
        
        #Can remove a bpm 
        self.assertEqual(update_chart(chart, bpm, remove = True), Result.SUCCESS)
        self.assertEqual(len(chart.sequence_data), 0)

    def test_update_chart_point(self):
        chart = new_chart()
        stepdict = new_step_dict(start_tick = 10, end_tick = 20, left_pos = 30, right_pos = 40, kind = 1, player_id =1)
        pointdict = new_point_dict(tick = 10, left_pos = 20, right_pos = 30, left_end_pos = 40, right_end_pos = 50)
        
        step1 = object_from_dict(stepdict)
        point1 = object_from_dict(pointdict)

        self.assertEqual(update_chart(chart, point1), Result.INVALID_LONG_POINT)

        self.assertEqual(update_chart(chart, point1, point_parent_step = step1), Result.NOTE_DOESNT_EXIST)
       
        #Can't remove point that isn't on a step
        update_chart(chart, step1)
        self.assertEqual(update_chart(chart, point1, point_parent_step = step1, remove = True), Result.NO_ACTION)
       
        #Can add a point to a step
        self.assertEqual(update_chart(chart, point1, point_parent_step = step1), Result.SUCCESS)
        self.assertEqual(len(chart.sequence_data[0].long_point), 1)
        
        #Can't add an identical point
        self.assertEqual(update_chart(chart, point1, point_parent_step = step1), Result.POINT_ALREADY_EXISTS)
        self.assertEqual(len(chart.sequence_data[0].long_point), 1)
    
        #Can remove a point 
        self.assertEqual(update_chart(chart, point1, point_parent_step = step1, remove = True), Result.SUCCESS)
        self.assertEqual(len(chart.sequence_data[0].long_point), 0)


if __name__ == "__main__":
    generateCompleteChart()
    generateTestChart()
    generateEffectSyncTest()

    unittest.main()
