import wpilib
import ctre
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

import robotmap

LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

#Constants for the kicker
PNCANID = 0
RFForward = 0
RFReverse = 1

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

        self.foot = RoboFoot(wpilib.DoubleSolenoid(PNCANID, RFForward, RFReverse))

        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

     

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
        
        forward = self.driver.getY(LEFT_HAND)
        
        rotation_value = self.driver.getX(RIGHT_HAND)
        
        forward = deadzone(forward, robotmap.deadzone)
        rotation_value = deadzone(rotation_value, robotmap.deadzone)

        self.myRobot.arcadeDrive(forward, rotation_value)

        #center_speed = deadzone(self.driver.getTriggerAxis(LEFT_HAND), robotmap.deadzone)
        left_in = 0
        right_in = 0
        
        if self.driver.getRawAxis(2) > 0:
            left_in = self.driver.getRawAxis(2)
        elif self.driver.getRawAxis(2) < 0:
            right_in = self.driver.getRawAxis(2)

        if self.operator.getAButtonPressed():
            self.foot.kick()
        
        if  self.operator.getAButtonReleased():
            self.foot.unkick()

        if self.driver.getRawAxis(2) > 0:
            self.center1.set(left_in)
            self.center2.set(-left_in)
        elif self.driver.getRawAxis(2) < 0:
            self.center1.set(-1)
            self.center2.set(1)
        elif self.driver.getRawAxis(3) != 0:
            self.center1.set(-1)
            self.center2.set(1)
        else:
            self.center1.set(0)
            self.center2.set(0)


        # print(right_in)
        # print(right_in * 1000000000000000000)
        # print(left_in)
        #self.setCenters(center_speed)

def deadzone(val, deadzone):
    if abs(val) < deadzone:
        return 0
    elif val < (0):
        x = ((abs(val) - deadzone)/(1-deadzone))
        return (-x)
    else:
        x = ((val - deadzone)/(1-deadzone))
        return (x)

# It's the Super RoboFoot class.
class RoboFoot:
    stateExtend = wpilib.DoubleSolenoid.Value.kForward
    stateRetract = wpilib.DoubleSolenoid.Value.kReverse
    def __init__(self, piston):
        self.piston = piston

    def kick(self):
        self.piston.set(RoboFoot.stateRetract)
    
    def unkick(self):
        self.piston.set(RoboFoot.stateExtend)

    
if __name__ == "__main__":
    wpilib.run(MyRobot)
