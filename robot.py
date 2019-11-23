import wpilib
import wpilib.drive
import ctre
import robotmap
from wpilib.interfaces import GenericHID


RIGHT_HAND = GenericHID.Hand.kRight
LEFT_HAND = GenericHID.Hand.kLeft


class Robot(wpilib.TimedRobot):

    def robotInit(self):
        front_left_motor = ctre.WPI_TalonSRX(robotmap.mecanum['front_left_motor'])  
        back_left_motor = ctre.WPI_TalonSRX(robotmap.mecanum['back_left_motor'])  
        front_right_motor = ctre.WPI_TalonSRX(robotmap.mecanum['front_right_motor'])  
        back_right_motor = ctre.WPI_TalonSRX(robotmap.mecanum['back_right_motor'])  

        front_left_motor.setInverted(True)
        #back_left_motor.setInverted(True)


        self.drive = wpilib.drive.MecanumDrive(
            front_left_motor,
            back_left_motor,
            front_right_motor,
            back_right_motor
        )

        self.drive.setExpiration(0.1)
        
        self.lstick = wpilib.XboxController(0)
        self.rstick = wpilib.XboxController(1)

        self.gyro = wpilib.AnalogGyro(1)

    #def teleopInit(self):
    #    self.xforward = 0
    #    self.yforward = 0


    """def operatorControl(self):
        Called when operation control mode is enabled

        while self.isOperatorControl() and self.isEnabled():
            self.drive.driveCartesian(
                self.lstick.getX(), self.lstick.getY(), self.rstick.getX(), 0
            )

            wpilib.Timer.delay(0.04)
    """
    
    def teleopPeriodic(self):
    
        """Called when operation control mode is enabled"""

       

        if not self.rstick.getXButton() or not self.lstick.getXButton():
            lspeed = deadzone(self.lstick.getX(LEFT_HAND), 0.2) 
            rspeed = deadzone(self.lstick.getY(LEFT_HAND), 0.2)
            rotate = self.lstick.getX(RIGHT_HAND)
        else:
            rotate = 0
            lspeed = 0
            rspeed = 0
        
        self.drive.driveCartesian(
            lspeed, rspeed, rotate, self.gyro.getAngle()
        )

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
    wpilib.run(Robot,physics_enabled=True)