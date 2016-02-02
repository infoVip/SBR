#!/usr/bin/python

import smbus
import math

class Accelerometer(object):
	def __init__(self,i2caddr=0x68):
	    
        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = i2caddr       # This is the address value read via the i2cdetect command
        
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(address, power_mgmt_1, 0)
    
    def read_byte(self,adr):
        return self.bus.read_byte_data(address, adr)
    
    def read_word(self,adr):
        high = self.bus.read_byte_data(address, adr)
        low = self.bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
        return val
    
    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    
    @staticmethod
    def dist(a,b):
        return math.sqrt((a*a)+(b*b))
    
    @staticmethod
    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)
    
    @staticmethod
    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)


    def gyro(self):

        print "gyro data"
        print "---------"
        
        gyro_xout = self.read_word_2c(0x43)
        gyro_yout = self.read_word_2c(0x45)
        gyro_zout = self.read_word_2c(0x47)
        
        print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
        print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
        print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

    def accelerometer(self):
        print
        print "accelerometer data"
        print "------------------"
        
        accel_xout = self.read_word_2c(0x3b)
        accel_yout = self.read_word_2c(0x3d)
        accel_zout = self.read_word_2c(0x3f)
        
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        
        print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
        print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
        print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
        
        print "x rotation: " , self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        print "y rotation: " , self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)