from time import sleep
import pigpio
import sys
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

pi.set_PWM_frequency(STEP2, 500)  # 500 pulses per second for motor 2

# Function to move stepper motor
def move_stepper_actuator(steps, direction, dir_pin, step_pin, enable_pin):
    pi.write(dir_pin, direction)  # Set direction
    pi.write(enable_pin, 0)  # Enable the stepper motor driver (0 = enabled)
    for _ in range(steps):
        pi.write(step_pin, 1)
        sleep(0.005)  # Control speed by adjusting the sleep time
        pi.write(step_pin, 0)
        sleep(0.005)
    pi.write(enable_pin, 1)  # Disable the motor after movement (1 = disabled)

def move_stepper_pcb(steps, direction, dir_pin, step_pin, enable_pin):
    pi.write(dir_pin, direction)  # Set direction
    pi.write(enable_pin, 0)  # Enable the stepper motor driver (0 = enabled)
    for _ in range(steps):  
        pi.write(step_pin, 1)
        sleep(0.0067)  # Control speed by adjusting the sleep time
        pi.write(step_pin, 0)
        sleep(0.0067)
    pi.write(enable_pin, 0)  # Disable the motor after movement (1 = disabled)

def move_servo(pulse_width):
    pi.set_servo_pulsewidth(SERVO_PWM, pulse_width)


try:
    # Move Motor 2 (new motor) by 1/8 rotation (25 steps at full step)
    for i in range(1):
        move_servo(500)  # Move servo to 1/4 of full range
        sleep(0.5)
        
        move_stepper_actuator(450, 1, DIR1, STEP1, ENABLE1)
        sleep(1)
        
        move_stepper_pcb(int(float(sys.argv[1]))*2, 1, DIR2, STEP2, ENABLE2)  # Forward
        sleep(1)  # Wait for 2 seconds
        
        move_servo(790)  # Move servo to 1/4 of full range
        sleep(0.5)
        
        move_stepper_actuator(450, 0, DIR1, STEP1, ENABLE1)
        sleep(1)
        
except KeyboardInterrupt:
    print("\nCtrl-C pressed. Stopping PIGPIO and exiting...")
finally:
    pi.set_PWM_dutycycle(STEP1, 0)  # PWM off for motor 1
    pi.set_PWM_dutycycle(STEP2, 0)  # PWM off for motor 2
    pi.stop()
  