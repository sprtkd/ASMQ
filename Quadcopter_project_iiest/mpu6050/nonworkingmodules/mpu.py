import smbus
import time
class MPU6050:
    
    gravity=9.80665
    address=0x68
    bus=smbus.SMBus(1)
    acc2g=16384.0
    acc4g=8192.0
    acc8g=4096.0
    acc16g=2048.0
    gyro250=131.0
    gyro500=65.5
    gyro1000=32.8
    gyro2000=16.4
    ar2g=0x00
    ar4g=0x08
    ar8g=0x10
    ar16g=0x18
    gr250=0x00
    gr500=0x08
    gr1000=0x10
    gr2000=0x18
    power=0x6B
    selfx=0x0D
    selfy=0x0E
    selfz=0x0F
    selfa=0x10
    accx1=0x3B
    accx2=0x3C
    accy1=0x3D
    accy2=0x3E
    accz1=0x3F
    accz2=0x40
    gyrox1=0x43
    gyrox2=0x44
    gyroy1=0x45
    gyroy2=0x46
    gyroz1=0x47
    gyroz2=0x48
    accelconfig=0x1C
    gyroconfig=0x1B
    def _init_(self):
##        self.address=address
        self.bus.write_byte_data(self.address,self.power,0x00)
    def readi2c(self,register):
        high=self.bus.read_byte_data(self.address,register)
        low=self.bus.read_byte_data(self.address,register+1)
        value=(high<<8)+low
        if (value>=0x8000):
            return -((65535-value)+1)
        else:
            return value
        
    def setaccelrange(self,accelrange):
        self.bus.write_byte_data(self.address,self.accelconfig,0x00)
        self.bus.write_byte_data(self.address,self.accelconfig,accelrange)
    def readaccelrange(self,raw=False):
        raw_data=self.bus.read_byte_data(self.address,self.accelconfig)
        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data==self.ar2g:
                return 2
            elif raw_data==self.ar4g:
                return 4
            elif raw_data==self.ar8g:
                return 8
            elif raw_data==self.ar16g:
                return 16
            else:
                return -1
    def getacceldata(self,g=False):
        x=self.readi2c(self.accx1)
        y=self.readi2c(self.accy1)
        z=self.readi2c(self.accz1)
        accelscalemodifier=None
        accelrange=self.readaccelrange(True)
        if accelrange==self.ar2g:
            accelscalemodifier=self.acc2g
        elif accelrange==self.ar4g:
            accelscalemodifier=self.acc4g    
        elif accelrange==self.ar8g:
            accelscalemodifier=self.acc8g
        elif accelrange==self.ar16g:
            accelscalemodifier=self.acc16g
        else:
            accelscalemodifier=self.acc2g

        x=x/accelscalemodifier
        y=y/accelscalemodifier
        z=z/accelscalemodifier

        if g is True:
            return {'x':x,'y':y,'z':z}
        elif g is False:
            x=x*self.gravity
            y=y*self.gravity
            z=z*self.gravity
            return {'x':x,'y':y,'z':z}
    def setgyrorange(self,gyro_range):
        self.bus.write_byte_data(self.address,self.gyroconfig,0x00)
        self.bus.write_byte_data(self.address,self.gyroconfig,gyro_range)
    def readgyrorange(self,raw=False):
        rawdata=self.bus.read_byte_data(self.address,self.gyroconfig)
        if raw is True:
            return rawdata
        elif raw is False:
            if rawdata==gr250:
                return 250
            elif rawdata==gr500:
                return 500
            elif rawdata==gr1000:
                return 1000
            elif rawdata==gr2000:
                return 2000
            else:
                return -1
    def getgyrodata(self):
        x=self.readi2c(self.gyrox1)
        y=self.readi2c(self.gyroy1)
        z=self.readi2c(self.gyroz1)
        gyroscalemodifier=None
        gyro_range=self.readgyrorange(True)
        if gyro_range==self.gr250:
            gyroscalemodifier=self.gyro250
        elif gyro_range==self.gr500:
            gyroscalemodifier=self.gyro500
        elif gyro_range==self.gr1000:
            gyroscalemodifier=self.gyro1000
        elif gyro_range==self.gr2000:
            gyroscalemodifier=self.gyro2000
        else:
            gyroscalemodifier=self.gyro250
        x=x/gyroscalemodifier
        y=y/gyroscalemodifier
        z=z/gyroscalemodifier
        return {'x':x,'y':y,'z':z}
    def getalldata(self):
        accel=getacceldata()
        gyro=getgyrodata()
        return [accel,gyro]

mpu=MPU6050()
t=time.time()
t1=time.time()
gyro_data=mpu.getgyrodata()
goffx=gyro_data['x']
goffy=gyro_data['y']
goffz=gyro_data['z']
Xangle=0
for i in range (0,100):
    tdiff=time.time()-t1
    td=time.time()-t
    t=time.time()
##    accel_data=mpu.getacceldata()
##    print ("Accelerometer Data")
##    print ("AccelX:",accel_data['x'])
##    print ("AccelY:",accel_data['y'])
##    print ("AccelZ:",accel_data['z'])
    gyro_data=mpu.getgyrodata()
    Xangle+=(td*(round(goffx-gyro_data['x'])))
##    print ("Gyroscope Data")
##    print ("GyroX:",(goffx-gyro_data['x']))
##    print ("GyroY:",(goffy-gyro_data['y']))
##    print ("GyroZ:",(goffz-gyro_data['z']))
    print ("Xangle",Xangle)
    print ("td",td)
    print ("time difference",tdiff)
    print ("************************************")
    
    
        
        
            
        
        
        
        
    
