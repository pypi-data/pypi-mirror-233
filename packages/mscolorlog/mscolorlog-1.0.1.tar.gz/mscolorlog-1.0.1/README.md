# MSColorLog
A highly customizable package that can ouput colored logs to the console.

---

![example](https://resources.sirin.net.cn/MarkDownImgs/coloredloggingeg.png)

## Usage:
### Importing the package:
```
import mscolorlog as cl
```
### Initializing the logger:
```
logger = cl.Logging([LOGGING LEVEL], [LOGGING ELEMENT1], [LOGGING ELEMENT2], ...)
```
## **Logging Levels:**
- Logging.DEBUG
- Logging.INFO
- Logging.WARNING
- Logging.ERROR
- Logging.CRITICAL

*NOTICE that the Logger will only output logs that are equal to or higher than the logging level.*

## **Logging Elements:**

Format: 
"&MODE:BACKGROUND:FOREGROUND:$VALUE" or "&MODE:BACKGROUND:FOREGROUND:TEXT"

### Modes:
- default
- highlight
- underline
- blink
- reverse
- invisible

*NOTICE that the modes may not compatible for all consoles*

Leave blank to use default mode

### Back/Foreground colors:
- black
- red
- green
- yellow
- blue
- purple
- cyan
- white

Leave blank to use default color

### Values:
- $info.processName
- $info.pid
- $info.time
- $type.type (Log level name)
- $message.message (Log message)

*Next, more values will be updated*

You can also put your own text in the value section
and the logger will output the text instead of the value.

NOTICE that "$" means the value is a variable, and the logger will output the value of the variable.
and "$$" means a "$" sign.

Also, color section can be omitted, and the logger will use the default color.

For example:
```
&underline::yellow:$$123
&::red:$$123
&:::$$123
$$123
```
The logger will output: $123 but with different colors and patterns.

**Change the color of log level:**

The Color of the Log Level can be changed by:
If the function isn't called, the logger will use the default color.
```
logger.setColor(MODE=PATTERN, MODEMsgToo=True/False, ...)
```
The `PATTERN` can be any color in the color list above, the format is the same as the logging elements. 

The `MODEMsgToo` means whether the logger will change the pattern of the log message too.

For example:
```
logger.setColor(info="&::red:", infoMsgToo=True)
```
The logger will change the color of the log level INFO to red, and the color of the log message to red too.
If you have set the color of the log message, this will override the previous setting.
You can call the function multiple times.

**Change the level of logger:**

You can use the following code to change the level of the logger:
```
 logger.setMode(MODE)
```

## Output Log Messages:
Use the following code to output log messages:
```
logger.pdebug(MESSAGE)
logger.pinfo(MESSAGE)
logger.pwarning(MESSAGE)
logger.perror(MESSAGE)
logger.pcritical(MESSAGE)
```

## Example:
Use the following code to output log messages like the image above:
```
import mscolorlog as cl

if __name__ == "__main__":
    log = cl.Logging(cl.Logging.WARNING,
                     "&::yellow:[", "&::green:$info.time", "&::yellow:] ",
                     "&::blue:$info.processName",
                     "&::blue:(", "&::blue:$info.pid", "&::blue:) ",
                     "$type.type", "&::cyan:> ", "&:black:white:$message.message")

    log.pdebug("debugMessage")
    log.pinfo("infoMessage")
    log.pwarning("warningMessage")
    log.perror("errorMessage")
    log.pcritical("criticalMessage")

    log.setMode(cl.Logging.DEBUG)
    log.setColor(critical="&::purple:", criticalMsgToo=False)

    log.pdebug("debugMessage")
    log.pinfo("infoMessage")
    log.pwarning("warningMessage")
    log.perror("errorMessage")
    log.pcritical("criticalMessage")
```
Life is short, I use Python.

HAVE FUN!