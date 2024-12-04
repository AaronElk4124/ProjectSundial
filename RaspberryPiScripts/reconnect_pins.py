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
# 
pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(ENABLE2, pigpio.OUTPUT)

pi.set_mode(SERVO_PWM, pigpio.OUTPUT)  # Servo PWM pin setup


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
        
def move_servo(pulse_width):
    pi.set_servo_pulsewidth(SERVO_PWM, pulse_width)
    
try:
    pi.write(ENABLE2, 0)
    move_servo(790)
    sleep(0.5)
        
    move_stepper_actuator(450, 0, DIR1, STEP1, ENABLE1)
    sleep(1)
    
    

        
except KeyboardInterrupt:
    print("\nCtrl-C pressed. Stopping PIGPIO and exiting...")
finally:
    pi.write(ENABLE1, 1)
    pi.write(ENABLE2, 0)
    pi.set_PWM_dutycycle(STEP1, 0)
    pi.set_PWM_dutycycle(STEP2, 0)
    pi.stop()