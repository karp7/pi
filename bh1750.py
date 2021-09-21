#!/usr/bin/python
#---------------------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bh1750.py
# Read data from a BH1750 digital light sensor.
#
# Author : Matt Hawkins
# Date   : 26/06/2018
#
# For more information please visit :
# https://www.raspberrypi-spy.co.uk/?s=bh1750
#
#---------------------------------------------------------------------
import smbus
import time
import subprocess

#from rpi_backlight import Backlight

# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)


class ShellCMD(object):
    def __init__(self,mcmd, icmd_ls):
        super(ShellCMD, self).__init__()
        self.mcmd = mcmd
        self.GetShells(icmd_ls)


    def GetShells(self,cmd_ls):

        for shell in cmd_ls:
            self.GetShell(shell)
        pass

    def GetShell(self,cmd):

        try:
            err = subprocess.run(cmd.split())
            # print("l_Level=",", err=",err.returncode)
        except:
            print("Помилка команди",cmd)
        pass

# функція відповідності освітлення в 0-1024
    def LxToY(self,Lx):
      result=(Lx*1024)/160
      if result<400:
        result=400
      return result

    def GetLight(self,xLevel):
      yLevel=self.LxToY(xLevel)
      lightLevel = self.mcmd+str(yLevel)
      self.GetShell(lightLevel)




def main():
  icmd=[
          'gpio -g pwm 18 1024',
          'gpio -g mode 18 pwm',
          'gpio pwmc 1000',
      ]
  mcmd='gpio -g pwm 18 '

  Display=ShellCMD(mcmd, icmd)
  while True:
    lightLevel=readLight()
    print("Light Level : " + format(lightLevel,'.2f') + " lx")

    Display.GetLight(lightLevel)

    time.sleep(0.5)

if __name__=="__main__":
   main()
