from time import sleep
import pigpio

# Motor 1 (Original motor)
DIR1 = 20     # Direction GPIO Pin for motor 1
STEP1 = 21    # Step GPIO Pin for motor 1
ENABLE1 = 12  # Enable GPIO Pin for motor 1

# Motor 2 (New motor)
DIR2 = 22     # Direction GPIO Pin for motor 2
STEP2 = 23    # Step GPIO Pin for motor 2
ENABLE2 = 24  # Enable GPIO Pin for motor 2

SERVO_PWM = 11  # PWM GPIO Pin for the servo motor


# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as output for both motors
pi.set_mode(DIR1, pigpio.OUTPUT)
pi.set_mode(STEP1, pigpio.OUTPUT)
pi.set_mode(ENABLE1, pigpio.OUTPUT)

pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(ENABLE2, pigpio.OUTPUT)

pi.set_mode(SERVO_PWM, pigpio.OUTPUT)  # Servo PWM pin setup

def move_stepper_pcb(steps, direction, dir_pin, step_pin, enable_pin):
    pi.write(dir_pin, direction)  # Set direction
    pi.write(enable_pin, 0)  # Enable the stepper motor driver (0 = enabled)
    for _ in range(steps):  
        pi.write(step_pin, 1)
        sleep(0.0067)  # Control speed by adjusting the sleep time
        pi.write(step_pin, 0)
        sleep(0.0067)
    pi.write(enable_pin, 0)  # Disable the motor after movement (1 = disabled)


try:
    # Move Motor 2 (new motor) by 1/8 rotation (25 steps at full step)
    for i in range(1):
        move_stepper_pcb(1, 1, DIR2, STEP2, ENABLE2)  # Forward
        sleep(0.001)  # Wait for 2 seconds

        
except KeyboardInterrupt:
    print("\nCtrl-C pressed. Stopping PIGPIO and exiting...")
finally:
    pi.set_PWM_dutycycle(STEP1, 0)  # PWM off for motor 1
    pi.set_PWM_dutycycle(STEP2, 0)  # PWM off for motor 2
    pi.stop()