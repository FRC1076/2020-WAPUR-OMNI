import wpilib
import ctre
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

import robotmap

LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""
        # object that handles basic drive operations
        self.leftVictor = ctre.WPI_VictorSPX(robotmap.omni['left_motor'])
        self.rightVictor = ctre.WPI_VictorSPX(robotmap.omni['right_motor'])
        

        self.left = wpilib.SpeedControllerGroup(self.leftVictor)
        self.right = wpilib.SpeedControllerGroup(self.rightVictor)

        self.centerVictor1 = ctre.WPI_VictorSPX(robotmap.omni['front_strafe'])
        self.centerVictor2 = ctre.WPI_VictorSPX(robotmap.omni['back_strafe'])

        self.center1 = wpilib.SpeedControllerGroup(self.centerVictor1)
        self.center2 = wpilib.SpeedControllerGroup(self.centerVictor2)

        self.myRobot = DifferentialDrive(self.left, self.right)
        

        self.myRobot.setExpiration(0.1)

        self.LEFT = GenericHID.Hand.kLeft
        self.RIGHT = GenericHID.Hand.kRight

        self.driver = wpilib.XboxController(0)

     

    def autonomousInit(self):
        #self.myRobot.tankDrive(0.8, 0.8)
        pass

    def autonomousPeriodic(self):
        # TODO: Add an auton
        #self.myRobot.tankDrive(1, 0.5)
        pass

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.myRobot.setSafetyEnabled(True)

    def setCenters(self, speed_value):
        self.center1.set(-speed_value)
        self.center2.set(speed_value)
    
    

    def teleopPeriodic(self):
    
        
        
        forward = -self.driver.getY(LEFT_HAND)
        
        rotation_value = self.driver.getX(RIGHT_HAND)
        
        forward = deadzone(forward, robotmap.deadzone)

        self.myRobot.arcadeDrive(forward, rotation_value)

        center_speed = deadzone(self.driver.getTriggerAxis(LEFT_HAND), robotmap.deadzone)

        self.setCenters(center_speed)


        
        


def deadzone(val, deadzone):
    if abs(val) < deadzone:
        return 0
    elif val < (0):
        x = ((abs(val) - deadzone)/(1-deadzone))
        return (-x)
    else:
        x = ((val - deadzone)/(1-deadzone))
        return (x)

if __name__ == "__main__":
    wpilib.run(MyRobot)