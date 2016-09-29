from mpu import MPU6050
sensor=MPU6050(0x68)
for i in range (0,50):
    accel_data=sensor.getacceldata()
    gyro_data=sensor.getgyrodata()
    print ("Accelerometer data")
    print ("x:"+str(accel_data['x']))
    print ("y:"+str(accel_data['y']))
    print ("z:"+str(accel_data['z']))
    print ("gyroscope data")
    print ("x:"+str(gyro_data['x']))
    print ("y:"+str(gyro_data['y']))
    print ("z:"+str(gyro_data['z']))
    
