import psutil
import os
import time


class LogError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        print("\033[5;;31mLOGGING ERROR: " + self.message + "\033[0m")


class Logging:
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    def __init__(self, mode, *structure):
        # STRUCTURE EXAMPLE:

        # modes = debug 1 | info 2 | warning 3 | error 4 | critical 5
        self.mode = None
        self.modeLV = 0

        self.types = {"debug": "DBUG", "info": "INFO", "warning": "WARN", "error": "EROR", "critical": "CRIT"}
        self.color = Logging.Color()
        self.info = Logging.Information()
        self.structure = structure
        self.domains = ["info", "type"]
        self.domainNames = {"info": self.info}
        # self.typeColors = {"debug": "&::cyan:", "info": "&::green:", "warning:": "&::yellow:", "error": "&::red:"}
        self.typeColors = {}
        # self.msgColorToo = {"debug": False, "info": False, "warning": True, "error": True, "critical": True}
        self.msgColorToo = {}
        self.setMode(mode)
        self.setColor()

    def setMode(self, mode):
        if mode == "debug":
            self.modeLV = 1
        if mode == "info":
            self.modeLV = 2
        if mode == "warning":
            self.modeLV = 3
        if mode == "error":
            self.modeLV = 4
        if mode == "critical":
            self.modeLV = 5
        self.mode = mode

    def setColor(self, debug="&::cyan:", debugMsgToo=False, info="&::green:", infoMsgToo=False, warning="&::yellow:",
                 warningMsgToo=True, error="&::red:", errorMsgToo=True, critical="&:red:black:", criticalMsgToo=True):
        self.typeColors["debug"] = debug
        self.msgColorToo["debug"] = debugMsgToo
        self.typeColors["info"] = info
        self.msgColorToo["info"] = infoMsgToo
        self.typeColors["warning"] = warning
        self.msgColorToo["warning"] = warningMsgToo
        self.typeColors["error"] = error
        self.msgColorToo["error"] = errorMsgToo
        self.typeColors["critical"] = critical
        self.msgColorToo["critical"] = criticalMsgToo

    def getStructrue(self, logType, message):
        output = []
        outputstr = ""

        for element in self.structure:

            if not element[0] == "&":
                element = "&:::" + element
            prefixes = element.split(":")
            contents = "".join(prefixes[3:])

            if contents[0] == "$":

                if contents[:2] == "$$":
                    txt = list(contents)
                    txt[:2] = "$"
                    text = "".join(txt)

                else:
                    cmd = contents[1:].split(".")

                    if len(cmd) > 2:
                        raise LogError("Var too long: " + contents)

                    try:
                        domain = cmd[0]
                        target = cmd[1]
                    except Exception:
                        raise LogError("Illegal param: " + str(element))

                    if domain == "type" or target == "type":
                        try:
                            text = self.types[logType]
                        except KeyError:
                            raise LogError("Unknown Log Type: " + logType)
                        prefixes = self.typeColors[logType].split(":")

                    elif domain == "message" or target == "message":
                        text = message
                        if self.msgColorToo[logType]:
                            prefixes = self.typeColors[logType].split(":")

                    elif domain == "info":
                        try:
                            r = self.Information.get(self.Information)
                            text = r[target]
                        except KeyError:
                            raise LogError("Unknown Element: " + target)

                    else:
                        raise LogError("Unknown var domain: " + domain)

            else:
                text = contents

            try:
                output.append(self.color.output(function=prefixes[0][1:], backcolor=prefixes[1], forecolor=prefixes[2],
                                                text=text))
            except Exception as e:
                raise LogError("Unexpected param " + str(e))

        for i in output:
            outputstr += i

        return outputstr

    class Color:
        def __init__(self):
            self.back = {"black": "40", "red": "41", "green": "42", "yellow": "43", "blue": "44", "purple": "45",
                         "cyan": "46",
                         "white": "47", "": ""}
            self.fore = {"black": "30", "red": "31", "green": "32", "yellow": "33", "blue": "34", "purple": "35",
                         "cyan": "36",
                         "white": "37", "": ""}
            self.func = {"default": "0", "highlight": "1", "underline": "4", "blink": "5", "reverse": "7",
                         "invisible": "8", "": ""}
            self.reset = "\033[0m"

        def RESET(self):
            print(self.reset, end="")

        def output(self, text="", function="default", backcolor="", forecolor="", reset=True):
            out = "\033[" + self.func[function] + ";" + self.back[backcolor] + ";" + self.fore[forecolor] + "m" + text
            if reset:
                out += self.reset
            return out

    class Information:
        def __init__(self):
            self.pid = None
            self.processName = None
            self.time = None
            self.infos = {}

        def get(self, pid=None, stampcut=16):
            self.pid = str(os.getppid())
            if pid is None:
                pid = self.pid
            self.processName = str(psutil.Process(int(pid)).name())
            self.time = str(time.time())
            self.infos = {"pid": self.pid, "processName": self.processName, "time": self.time[:stampcut]}
            return self.infos

    def refresh(self, domain="ALL"):
        if domain == "ALL":
            for i in self.domainNames:
                self.domainNames[i].get()
            return "ALL"
        else:
            return self.domainNames[domain].get()

    def pdebug(self, text):
        if self.modeLV <= 1:
            print(self.getStructrue("debug", text))

    def pinfo(self, text):
        if self.modeLV <= 2:
            print(self.getStructrue("info", text))

    def pwarning(self, text):
        if self.modeLV <= 3:
            print(self.getStructrue("warning", text))

    def perror(self, text):
        if self.modeLV <= 4:
            print(self.getStructrue("error", text))

    def pcritical(self, text):
        if self.modeLV <= 5:
            print(self.getStructrue("critical", text))
