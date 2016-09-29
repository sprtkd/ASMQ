def autoGimbalUpdate():
    if(IsAutogimbal.get()):
        updatePanGimbal(-angle_x)
        updateTiltGimbal(-angle_y)

    
