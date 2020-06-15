import smbus
import math
import time


class quadMPU6050:
    GYRO_SCALE = 131.0
    ACCEL_SCALE = 16384.0
    I2C_ADDRESS = 0x68  # This is the I2C_ADDRESS value read via the i2cdetect command
    I2C_PORT = 1
    POWER_MGMT_1 = 0x6b
    POWER_MGMT_2 = 0x6c
    X_ERROR_INIT = 2.0
    Y_ERROR_INIT = 5.0
    Z_ERROR_INIT = 0.0
    UPDATE_WEIGHTAGE_1 = 0.95
    UPDATE_WEIGHTAGE_2 = 1 - UPDATE_WEIGHTAGE_1

    bus = None
    now = None
    angvelerrorz = 0.0
    x_error = 0.0
    y_error = 0.0
    angle_x = 0
    angle_y = 0
    linacc_x = 0.0
    linacc_y = 0.0
    angularVelocity_z = 0.0
    last_x = 0.0
    last_y = 0.0

    def __init__(self):
        self.bus = smbus.SMBus(self.I2C_PORT)
        self.bus.write_byte_data(self.I2C_ADDRESS, self.POWER_MGMT_1, 0)
        self.resetMPU(True)

    def resetMPU(self, ifResetCalibration=False):
        self.now = time.time()
        if ifResetCalibration:
            self.x_error = self.X_ERROR_INIT
            self.y_error = self.Y_ERROR_INIT
            self.angvelerrorz = self.Z_ERROR_INIT
        (_, _, gyro_scaled_z, accel_scaled_x,
         accel_scaled_y, accel_scaled_z) = self.__read_all()
        self.last_x = self.__get_x_rotation(
            accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.last_y = self.__get_y_rotation(
            accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.angvelerrorz = gyro_scaled_z

    def calibrateMpu(self):
        (_, _, _,
         accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.__read_all()
        self.x_error = self.__get_x_rotation(
            accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.y_error = self.__get_y_rotation(
            accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.resetMPU()

    def updateMpu6050(self):
        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z,
         accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.__read_all()
        rotation_x = self.__get_x_rotation(
            accel_scaled_x, accel_scaled_y, accel_scaled_z)
        rotation_y = self.__get_y_rotation(
            accel_scaled_x, accel_scaled_y, accel_scaled_z)
        dtime = time.time()-self.now
        self.now = time.time()
        self.last_x = (self.UPDATE_WEIGHTAGE_1*(self.last_x+(gyro_scaled_x*dtime))) + \
            (self.UPDATE_WEIGHTAGE_2*rotation_x)
        self.last_y = (self.UPDATE_WEIGHTAGE_1*(self.last_y+(gyro_scaled_y*dtime))) + \
            (self.UPDATE_WEIGHTAGE_2*rotation_y)
        self.angle_x = -(self.last_x-self.x_error)
        self.angle_y = -(self.last_y-self.y_error)
        self.linacc_x = (accel_scaled_x -
                         (math.sin(math.radians(self.angle_y))))*9.81  # m/s^2
        self.linacc_y = (accel_scaled_y +
                         (math.sin(math.radians(self.angle_x))))*9.81  # m/s^2
        self.angularVelocity_z = -(gyro_scaled_z-self.angvelerrorz)

    def __read_all(self):
        raw_gyro_data = self.bus.read_i2c_block_data(self.I2C_ADDRESS, 0x43, 6)
        raw_accel_data = self.bus.read_i2c_block_data(
            self.I2C_ADDRESS, 0x3b, 6)
        gyro_scaled_x = self.__twos_compliment(
            (raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.GYRO_SCALE
        gyro_scaled_y = self.__twos_compliment(
            (raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.GYRO_SCALE
        gyro_scaled_z = self.__twos_compliment(
            (raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.GYRO_SCALE
        accel_scaled_x = self.__twos_compliment(
            (raw_accel_data[0] << 8) + raw_accel_data[1]) / self.ACCEL_SCALE
        accel_scaled_y = self.__twos_compliment(
            (raw_accel_data[2] << 8) + raw_accel_data[3]) / self.ACCEL_SCALE
        accel_scaled_z = self.__twos_compliment(
            (raw_accel_data[4] << 8) + raw_accel_data[5]) / self.ACCEL_SCALE
        return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)

    def __twos_compliment(self, val):
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def __dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def __get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.__dist(y, z))
        return -math.degrees(radians)

    def __get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.__dist(x, z))
        return math.degrees(radians)
