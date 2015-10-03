import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# Define constants
SEC_PER_TURN = 3   # Seconds required to complete one full turn
SEC_PER_MOVE = 4   # Seconds required to move 10cm

# Define motor pins
Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2A = 23
Motor2B = 21
Motor2E = 19

# Setup motor pin output
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)


def moveBot(direction, distance):

    if direction == 'forward':
        print "Going forwards ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_MOVE)

    elif direction == 'backward':
        print "Going backwards ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_MOVE)

    elif direction == 'turnleft':
        print "Turning Left ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_TURN)

    elif direction == 'turnright':
        print "Turning Right ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_TURN)

    else:
        print "ERROR: Wrong direction input"

    print "Stopping ..."
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.LOW)

    GPIO.cleanup()
    return


def main():

    moveBot('forward', 1)  # Move forward 1 unit (10 cm)
    moveBot('turnleft', 1)  # Make one complete turn

if __name__ == '__main__':
    main()
