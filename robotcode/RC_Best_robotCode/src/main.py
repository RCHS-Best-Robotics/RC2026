# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       matth                                                        #
# 	Created:      9/25/2026, 3:58:52 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
controller=Controller(PRIMARY)

brain.screen.print("new code ARMED")

motor1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

if controller.buttonR1.pressing():
       
        motor1.spin(FORWARD, 60, PERCENT)
        brain.screen.print("MOTOR SPINNING")
