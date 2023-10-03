# Test
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
