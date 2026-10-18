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

# Testing and brain print code
brain.screen.clear_screen()
brain.screen.set_cursor(1,1)
brain.screen.print("Baklava 13 by Rock Canyon BEST") 
mode = "manual"
switch_stick = controller.axis1.position()

brain.screen.new_line()
brain.screen.print("Mode: " + mode)

controller.screen.clear_screen()
controller.screen.set_cursor(1, 1)


# Motor definitions
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
forklift_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False) # Most likely gear ratios may need to be changed. max is 36:1


# Function definitions for autonomous mode
turn_left = lambda: (left_motor.spin(FORWARD, 0, PERCENT), right_motor.spin(FORWARD, 100, PERCENT))
turn_right = lambda: (left_motor.spin(FORWARD, 100, PERCENT), right_motor.spin(FORWARD, 0, PERCENT))
forward_move = lambda: (left_motor.spin(FORWARD, 100, PERCENT), right_motor.spin(FORWARD, 100, PERCENT))
backward_move = lambda: (left_motor.spin(REVERSE, 100, PERCENT), right_motor.spin(REVERSE, 100, PERCENT))



# Main control loop
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
    break

# 1. Define the action you want to take when movement happens
def handle_joystick_move():
    current_pos = controller.axis1.position() == 0
    mode = "auto"
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(mode)
    wait(20,MSEC)

# 2. Register the callback function to the axis event handler
# This binds your function to Axis 1 so it fires automatically upon changes
controller.axis1.changed(handle_joystick_move)
         



def Mode():
     controller.screen.print("Mode")
     Mode = ("Manual Mode")