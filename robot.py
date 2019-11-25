import wpilib
import wpilib.drive
import ctre
import robotmap
from wpilib.interfaces import GenericHID
from subsystems.BallManipulator import BallManipulator

RIGHT_HAND = GenericHID.Hand.kRight
LEFT_HAND = GenericHID.Hand.kLeft


class Robot(wpilib.TimedRobot):

    def robotInit(self):
        front_left_motor = ctre.WPI_TalonSRX(robotmap.mecanum['front_left_motor'])  
        back_left_motor = ctre.WPI_TalonSRX(robotmap.mecanum['back_left_motor'])  
        front_right_motor = ctre.WPI_TalonSRX(robotmap.mecanum['front_right_motor'])  
        back_right_motor = ctre.WPI_TalonSRX(robotmap.mecanum['back_right_motor'])  

        self.centerVictor1 = ctre.WPI_VictorSPX(robotmap.ball_manipulator['CENTER_1_ID'])
        self.centerVictor2 = ctre.WPI_VictorSPX(robotmap.ball_manipulator['CENTER_2_ID'])

        front_left_motor.setInverted(True)
        #back_left_motor.setInverted(True)


        self.center1 = wpilib.SpeedControllerGroup(self.centerVictor1)
        self.center2 = wpilib.SpeedControllerGroup(self.centerVictor2)

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

        self.ballManipulator = BallManipulator(ctre.WPI_VictorSPX(robotmap.ball_manipulator['BALL_MANIP_ID']))

    def teleopInit(self):
        pass


    def operatorControl(self):
        pass

    def setCenters(self, speed_value):
        self.center1.set(-speed_value)
        self.center2.set(speed_value)


    def teleopPeriodic(self):
    
        """Called when operation control mode is enabled"""
        ballMotorSetPoint = 0

        if self.driver.getBumper(LEFT_HAND):
            ballMotorSetPoint = 1.0
        elif self.driver.getBumper(RIGHT_HAND):
            ballMotorSetPoint = -1.0
        else:
            ballMotorSetPoint = 0.0
       

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

        center_speed = self.driver.getX(self.RIGHT)

        self.setCenters(self.deadzone(center_speed, self.DEADZONE))

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