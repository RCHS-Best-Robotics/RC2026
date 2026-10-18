# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       matth                                                        #
# 	Created:      9/25/2026, 3:58:52 PM                                        #
# 	Description:  V5 project
#   Version:      Dulce de Leche 2                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from token import PERCENT


from vex import * 
import time

# Brain should be defined by default
brain=Brain()
controller=Controller(PRIMARY)

# Set the mode
mode = "manual"
drive_mode = "arcade"

DEADZONE = 5 #Deadzone for joystick inputs
FORKLIFT_SPEED = 60

# Testing and brain print code
brain.screen.clear_screen()
brain.screen.set_cursor(1,1)
brain.screen.print("Dulce de Leche 2 by Rock Canyon BEST") 

brain.screen.new_line()
brain.screen.print("Mode: " + mode)

# Motor definitions
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
forklift_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False) # Most likely gear ratios may need to be changed. max is 36:1

# HELPER FUNCTIONS
def clamp(value):
    return max(-100, min(100, value))

def apply_deadzone(value):
    if abs(value) < DEADZONE:
        return 0
    return value

def spin_motor(motor, speed, stopping=BRAKE):
    speed = clamp(speed)

    if speed == 0:
        motor.stop(stopping)
    elif speed > 0:
        motor.spin(FORWARD, speed, PERCENT)
    else:
        motor.spin(REVERSE, -speed, PERCENT)

def drive(left_speed, right_speed):
    spin_motor(left_motor, left_speed)
    spin_motor(right_motor, right_speed)

def update_display():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Dulce de Leche 2 by Rock Canyon BEST")
    brain.screen.new_line()
    brain.screen.print("Mode: " + mode)
    brain.screen.new_line()
    brain.screen.print("Drive Mode: " + drive_mode)

    controller.screen.clear_screen()
    controller.screen.set_cursor(1,1)
    controller.screen.print("Mode: "+ mode)
    controller.screen.set_cursor(2,1)
    controller.screen.print("Drive Mode: "+ drive_mode)

# BUTTON EVENTS

def toggle_mode():
    global mode

    # flipping command
    if mode == "manual":
        mode = "auto"
    else:
        mode = "manual"

    drive (0,0) # stop motors when switching modes
    forklift_motor.stop(HOLD) # stop forklift motor when switching modes
    update_display()

def toggle_drive_mode():
    global drive_mode

    if mode != "manual":
        return  # Only allow drive mode toggle in manual mode
    
    # flipping command
    if drive_mode == "arcade":
        drive_mode = "tank"
    else:
        drive_mode = "arcade"

    drive(0,0)
    update_display()

# toggles
controller.buttonA.pressed(toggle_mode)
controller.buttonB.pressed(toggle_drive_mode)

update_display()

# Main control loop
while True:
    if mode == "manual":
        if drive_mode == "arcade":
            drive_power = apply_deadzone(controller.axis3.position())
            turn_power = apply_deadzone(controller.axis4.position())

            left_speed = drive_power + turn_power
            right_speed = drive_power - turn_power

            #Preserve steering ratio at high inputs
            max_speed = max(
                100,
                abs(left_speed),
                abs(right_speed)
            )

            left_speed = (left_speed / max_speed) * 100
            right_speed = (right_speed / max_speed) * 100

        elif drive_mode == "tank":
            left_speed = apply_deadzone(controller.axis3.position())
            right_speed = apply_deadzone(controller.axis2.position())
        drive(left_speed, right_speed)

        if controller.buttonL1.pressing():
            spin_motor(forklift_motor, FORKLIFT_SPEED, HOLD)
        elif controller.buttonL2.pressing():
            spin_motor(forklift_motor, -FORKLIFT_SPEED, HOLD)
        else:
            forklift_motor.stop(HOLD)
        
    elif mode == "auto":
        # now we in auto mode
        # Function definitions for autonomous mode
        forklift_motor.stop(HOLD)  # Stop the forklift motor in auto mode

        if controller.buttonUp.pressing():
            drive(10,10)
        elif controller.buttonDown.pressing():
            drive(-10,-10)
        elif controller.buttonLeft.pressing():
            drive(-10,10)
        elif controller.buttonRight.pressing():
            drive(10,-10)
        else:
            drive(0,0)

wait(20,MSEC)