from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

# Define constants
SEC_PER_TURN = 10   # Seconds required to complete one full turn
SEC_PER_MOVE = 1  # Seconds required to move 10cm
MOTOR_DEFAULT_PWR = 30  # Default starting power for the motor
MOTOR_OFFSET_PWR = -1  # Difference between Motor 1 and Motor 2

# Define motor pins
Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2A = 15
Motor2B = 13
Motor2E = 11

   # Setup motor pin output
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

# Output low signal
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2A, GPIO.LOW)
GPIO.output(Motor2B, GPIO.LOW)
GPIO.output(Motor2E, GPIO.LOW)


# Change speed of motor by controlling duty cycle
# def speed(num):
#     E1.ChangeDutyCycle(num)
#     E2.ChangeDutyCycle(num + MOTOR_OFFSET_PWR)
#     return


def moveBot(direction, distance, num):

    # Initialize PWM for  both motors
    E1 = GPIO.PWM(Motor1E, 100)
    E2 = GPIO.PWM(Motor2E, 100)

    # Start both sowftware PWMs
    E1.start(num)
    E2.start(num + MOTOR_OFFSET_PWR)

    # Alternatively send a HIGH signal for 100%
    # GPIO.output(Motor1E, GPIO.HIGH)
    # GPIO.output(Motor2E, GPIO.HIGH)

    if direction == 'forward':
        print "Going forwards ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)

        sleep(distance * SEC_PER_MOVE)

    elif direction == 'backward':
        print "Going backwards ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)

        sleep(distance * SEC_PER_MOVE)

    elif direction == 'turnleft':
        print "Turning Left ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)

        sleep((distance / 360) * SEC_PER_TURN)

    elif direction == 'turnright':
        print "Turning Right ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)

        sleep((distance / 360) * SEC_PER_TURN)

    else:
        print "ERROR: Wrong direction input"

    print "Stopping ..."

    E1.stop()
    E2.stop()

    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.LOW)

    return


def clean():  # Cleanup GPIO output
    E1.stop()
    E2.stop()
    GPIO.cleanup()
    return


def main():

    start()
    moveBot('forward', 1, MOTOR_DEFAULT_PWR)  # Move forward 1 unit (10 cm)
    moveBot('turnleft', 360, MOTOR_DEFAULT_PWR)  # Make one complete turn
    clean()

if __name__ == '__main__':
    main()
