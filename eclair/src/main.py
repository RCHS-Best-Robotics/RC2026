# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       matth                                                        #
# 	Created:      10/19/2026, 8:09:51 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import time

# Brain should be defined by default
brain=Brain()
controller = Controller(PRIMARY)
global display_screen

# Set variables
mode = "manual"
drive_mode = "arcade"
mult_speed = 1
display_screen = "main"

DEADZONE = 5 #Deadzone for joystick inputs
FORKLIFT_SPEED = 60

# Port configurations
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
forklift_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False) # Most likely gear ratios may need to be changed. max is 36:1
ai_vision = AiVision(Ports.PORT10, AiVision.ALL_TAGS)

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
    spin_motor(left_motor, (left_speed * mult_speed))
    spin_motor(right_motor, (right_speed * mult_speed))

def update_display():
    if display_screen == "main":
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("Eclair 2 by Rock Canyon BEST")
        brain.screen.new_line()
        brain.screen.print("Mode: " + mode)
        brain.screen.new_line()
        brain.screen.print("Drive Mode: " + drive_mode)
        brain.screen.new_line()
        brain.screen.print("Speed: " + str(mult_speed) + "x")

        controller.screen.clear_screen()
        controller.screen.set_cursor(1,1)
        controller.screen.print("Mode: "+ mode)
        controller.screen.set_cursor(2,1)
        controller.screen.print("Drive Mode: "+ drive_mode)
        controller.screen.set_cursor(3,1)
        controller.screen.print("Speed: " + str(mult_speed) + "x")
    elif display_screen == "vision":
        if tags:
            # Process the first detected tag
            tag = tags[0]
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("Tag ID: " + str(tag.id))
            brain.screen.new_line()
            brain.screen.print("Center X: " + str(tag.centerX))
            brain.screen.new_line()
            brain.screen.print("Center Y: " + str(tag.centerY))
        else:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("No tags detected")

# BUTTON EVENTS

def toggle_display():
    global display_screen

    if display_screen == "main":
        display_screen = "vision"
    elif display_screen == "vision":
        display_screen = "main"
update_display()

def toggle_mode():
    global mode
    global display_screen

    # flipping command
    if mode == "manual":
        mode = "auto"
    else:
        mode = "manual"

    drive (0,0) # stop motors when switching modes
    forklift_motor.stop(HOLD) # stop forklift motor when switching modes
    display_screen = "main"
    update_display()

def toggle_drive_mode():
    global drive_mode
    global display_screen

    if mode != "manual":
        return  # Only allow drive mode toggle in manual mode
    
    # flipping command
    if drive_mode == "arcade":
        drive_mode = "tank"
    else:
        drive_mode = "arcade"

    drive(0,0)
    display_screen = "main"
    update_display()

def toggle_mult_speed():
    global mult_speed
    global display_screen
    
    if mult_speed == 1:
        mult_speed = 2
    elif mult_speed == 2:
        mult_speed = 0.5
    else:
        mult_speed = 1

    drive(0,0)
    display_screen = "main"
    update_display()



# toggles
controller.buttonA.pressed(toggle_mode)
controller.buttonB.pressed(toggle_drive_mode)
controller.buttonX.pressed(toggle_mult_speed)
controller.buttonY.pressed(toggle_display)
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
            
        if controller.buttonL1.pressing():
            spin_motor(forklift_motor, FORKLIFT_SPEED, HOLD)
        elif controller.buttonL2.pressing():
            spin_motor(forklift_motor, -FORKLIFT_SPEED, HOLD)
        else:
            forklift_motor.stop(HOLD)
        wait(20, MSEC)

    elif mode == "auto":
        # now we in auto mode
        # Function definitions for autonomous mode
        forklift_motor.stop(HOLD)  # Stop the forklift motor in auto mode
        mult_speed = 1  # Reset speed multiplier in auto mode

        #AI Vision setup
        tags = ai_vision.take_snapshot(AiVision.ALL_TAGS)
        display_screen = "vision"

        update_display() # be sure to press Y to toggle between the AI vision display and the main display
        
    wait(20, MSEC)




