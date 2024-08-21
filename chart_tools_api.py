from chart_tools import *
import sys

class command_struct:
     def __init__(self):
         self.attribute = None #Attribute to alter
         self.command = None #Command to do to that attribute 
         self.args = [] #Any relevant arguments
         self.unparsed = None #The command unparsed (for useful debugging)

     commands = {
        "add": "add",
        "change": "change",
        "remove" :"remove",
        "get": "get",
        "load": "load",
        "init" : "init",
        "save": "save",
        "usage": "usage"
    }

class Session:
    def __init__(self):
        self.chart = None


def change_chart(command: command_struct, session: Session): 
    if command.command == command_struct.commands["load"]:
        try:
            session.chart = Chart(xml.etree.ElementTree.parse(command.args[0]).getroot())
        except:
            return Result.CHART_PARSING_ERROR

        return Result.SUCCESS

    if command.command == command_struct.commands["init"]:
        session.chart = Chart()
        return Result.SUCCESS

    if command.command == command_struct.commands["get"]:
        response = ""
        for note in session.chart.steps:
            response += "note {} {} {} {} {} {}\n".format(note.start_tick, note.end_tick, note.left_pos, note.right_pos, note.kind, note.player_id)

        return response

    if command.command == command_struct.commands["save"]:
        return session.chart.save(command.args[0]) 

    print("Usage: chart (load, init, save) (chart to load if applicable / filename of chart to save)")    
    return Result.NO_ACTION


def note(command: command_struct, session: Session):
    thisNote = stepXML(createEmptyStepXML())
    thisNote.start_tick = command.args[0]
    thisNote.end_tick = command.args[1]
    thisNote.left_pos = command.args[2]
    thisNote.right_pos = command.args[3]
    thisNote.kind = command.args[4]
    thisNote.player_id = command.args[5]

    if command.command == command_struct.commands["add"]:
        return session.chart.addNoteRaw(thisNote) 

    if command.command == command_struct.commands["remove"]:
        return session.chart.removeNote(thisNote) 
    
    print("Usage: note (add, remove) start_tick end_tick left_pos right_pos kind player_id")


def change_bpm(command: command_struct, session: Session):
    bpmsliced = command.args[0].split(".")
    newBPM = BPM(int(bpmsliced[0]))
    if len(bpmsliced) == 2:
        newBPM.bpmDecimals = bpmsliced[1][0:2]

    try:
        bpmraw = int(command.args[0])
        tick = command.args[1]
    except ValueError:
        return Result.TYPE_ERROR 

    if command.command == command_struct.commands["add"]:
        return session.chart.addBPM_Raw(bpmraw, tick)

    if command.command == command_struct.commands["remove"]:
        removeBPM = bpmXML(createEmptyBPMXML())
        removeBPM.tick = tick
        removeBPM.bpm = bpmraw
        return session.chart.removeBPM(removeBPM)

    print("Usage: bpm (add, remove) (bpm) (tick from which this bpm applies)")

def measure(command: command_struct, session: Session):
    newMeasure = measureXML(createEmptyMeasureXML())
    newMeasure.num = command.args[0]
    newMeasure.denomi = command.args[1]
    newMeasure.tick = command.args[2]

    if command.command == command_struct.commands["add"]:
        return session.chart.addMeasureRaw(newMeasure)

    if command.command == command_struct.commands["remove"]:
        return session.chart.removeMeasure(newMeasure)

    print("Usage: measure (add, remove) numerator denominator (starting tick)")   
    return Result.NO_ACTION

functionMap = {
    "chart": change_chart,
    "note": note,
    "bpm": change_bpm,
    "measure": measure,
    "time_unit": None
}


def dispatch_command(command: command_struct, session: Session):
    if command.attribute not in functionMap.keys():
        return "Invalid command: " + str(command.attribute)
    
    if session.chart is None and not (command.command == command_struct.commands["load"] or command.command == command_struct.commands["init"]): 
        return Result.CHART_NOT_LOADED

    return functionMap[command.attribute](command, session)


def parse_command(command: str):
    split = command.split()
    parsedCommand = command_struct()
    parsedCommand.attribute = split[0]
    parsedCommand.command = split[1]
    parsedCommand.args = split[2:]
    parsedCommand.unparsed = command

    return parsedCommand


if __name__ == "__main__":
    session = Session()
  
    if sys.argv[1] != "init":
        result = change_chart(parse_command("chart load {}".format(sys.argv[1])), session)
    else:
        result = change_chart(parse_command("chart init"), session) 

    if result != Result.SUCCESS:
        print(result)
        exit()

    command = ""
    for arg in sys.argv[3:]:
        if arg == ":":
            if command != "":
                result = dispatch_command(parse_command(command), session)
                if type(result) == str:
                    print(result)
                elif result != Result.SUCCESS:
                    print(result)
                    break

            command = ""
            continue

        command += arg + " "

    dispatch_command(parse_command(command), session)

    if type(result) == str:
        print(result)
    elif result != Result.SUCCESS:
        print(result)

    session.chart.save(sys.argv[2])
