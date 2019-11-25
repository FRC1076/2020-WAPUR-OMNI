class BallManipulator:
    """
    Manipulator wraps a motor controller that gathers and spits
    out the cargo balls.
    """
    def __init__(self, motor):
        self.motor = motor

    def gather(self, speed = GATHER_SPEED):
        self.motor.set(speed)

    def spit(self, speed = SPIT_SPEED):
        self.motor.set(speed)

    def stop(self):
        self.motor.set(STOP_SPEED)

    def set(self, setValue):
        """
        Direct control to be used with a controller
        that puts out f, 0, and -f for gather, stop,
        and spit, respectively.
        """
        self.motor.set(setValue)