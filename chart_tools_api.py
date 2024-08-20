from chart_tools import *

chart = None

class command_struct:
    commands = {
        "add": "add",
        "change": "change",
        "remove" :"remove",
        "get": "get",
        "load": "load",
        "init" : "init",
        "usage": "usage"
    }

    self.attribute = None #Attribute to alter
    self.command = None #Command to do to that attribute 
    self.args = [] #Any relevant arguments



#things to test:
#bpm parsing works (when there is no decimal) (when there are more than two places after the decimal (extras are ignored))
#function fails (when you add a bpm at a tick where there is already a bpm) (bpm is out of range) (removing a bpm that doesnt exist)
#function succeeds (adding multiple bpms to a song)
def change_bpm(args: command_struct):
    bpmsliced = args.args[0].split(".")
    newBPM = BPM(int(bpmspliced[0]))
    if len(bpmsliced) == 2:
        newBPM.bpmDecimals = bpmsliced[1][0:2]

    newBPM.timeSigNum = args[1]
    bpm.timeSigDenomi = args[2]
    tick = args[3]

    if args.command == command_struct.commands["add"]:
        return chart.addBPM(newBPM, tick) 

    if args.command == command_struct.commands["remove"]:
        return Result.NO_ACTION 

    if args.command == command_struct.commands["change"]:
        return Result.NO_ACTION

    print("Usage: bpm (add, change, remove) (bpm, supports up to 2 decimal places) (time signature numerator) (time signature denominator) (tick from which this bpm applies)")

def change_chart(args: command_struct): 
    if args.command == command_struct.commands["load"]:
        try:
            chart = xml.etree.ElementTree.parse(pathToChart).getroot()
        except:
            return Result.CHART_PARSING_ERROR

        return Result.SUCCESS

    if args.command == command_struct.commands["init"]:
        chart = Chart()
        return Result.SUCCESS
    
    print("Usage: chart (load, init) (chart to load, if applicable)")    
    return Result.NO_ACTION


functionMap = {
    "chart": change_chart,
    "note": "note",
    "jump": "jump",
    "down": "down",
    "bpm": change_bpm,
    "measure": None
    "time_unit": "time_unit"
}


def dispatch_command(command: str, args: list) -> str:
    if command not in functionMap.keys():
        return "Invalid command"
    
    if chart is None and command != "init" or command != "set_chart":
        return Result.CHART_NOT_LOADED


    functions[command](args)

    return "asdf"


if __name__ == "__main__":
    pass
