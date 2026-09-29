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

brain.screen.print("new code ARMED. Today's date is 9/29/2026")

left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
forklift_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False) # Most likely gear ratios may need to be changed

while True:

    drive_power = controller.axis3.position()  # Forward / Backward
    turn_power = controller.axis4.position()   # Left / Right
    forklift_power = controller.axis2.position() # Up / Down
    
    # Arcade Drive Math: Combine drive and turn values
    left_speed = drive_power + turn_power
    right_speed = drive_power - turn_power
    

    # Spin the motors at the calculated speeds
    left_motor.spin(FORWARD, left_speed, PERCENT)
    right_motor.spin(FORWARD, right_speed, PERCENT)
    forklift_motor.spin(FORWARD, forklift_power, PERCENT)
   
    wait(20,MSEC)