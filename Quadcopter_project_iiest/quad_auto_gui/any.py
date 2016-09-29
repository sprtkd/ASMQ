inputThrottle=0
inputRoll=0
inputYaw=0

quadRelaySet(mode)
inputPitch=0


def updatePanGimbal(PanGimbalValStr):
    float(PanGimbalValStr)
def updateTiltGimbal(TiltGimbalValStr):
    float(TiltGimbalValStr)

    pid()

    changeAllMotorsThrottleFunc()
panGimbal.set(90)
    tiltGimbal.set(90)
