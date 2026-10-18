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
import time

# Brain should be defined by default
brain=Brain()
controller=Controller(PRIMARY)

# Set the mode
mode = "manual"

# Testing and brain print code
brain.screen.clear_screen()
brain.screen.set_cursor(1,1)
brain.screen.print("Creme Brulee 1 by Rock Canyon BEST") 

#switch_stick = controller.axis1.position()

brain.screen.new_line()
brain.screen.print("Mode: " + mode)

controller.screen.clear_screen()
controller.screen.set_cursor(1, 1)
brain.screen.print("Mode: " + mode)


# Motor definitions
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
forklift_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False) # Most likely gear ratios may need to be changed. max is 36:1


# Function definitions for autonomous mode
turn_left = lambda: (left_motor.spin(FORWARD, 0, PERCENT), right_motor.spin(FORWARD, 100, PERCENT))
turn_right = lambda: (left_motor.spin(FORWARD, 100, PERCENT), right_motor.spin(FORWARD, 0, PERCENT))
forward_move = lambda: (left_motor.spin(FORWARD, 100, PERCENT), right_motor.spin(FORWARD, 100, PERCENT))
backward_move = lambda: (left_motor.spin(REVERSE, 100, PERCENT), right_motor.spin(REVERSE, 100, PERCENT))

# EVENTS

# A button switch
def toggle_mode():
    global mode

    # flipping command
    if mode == "manual":
        mode = "auto"
    else:
        mode = "manual"

    # update el brain
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Mode: "+ mode)

    # update el controller
    controller.screen.clear_screen()
    controller.screen.set_cursor(1,1)
    controller.screen.print("Mode: "+ mode)

# toggle is A button
controller.buttonA.pressed(toggle_mode)

# Main control loop
while True:
    if mode == "manual":
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
    elif mode == "auto":
        # now we in auto mode
    
        wait(20,MSEC)

